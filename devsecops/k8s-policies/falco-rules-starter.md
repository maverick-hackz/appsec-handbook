# Falco Starter Rules

Falco watches kernel events (syscalls, K8s audit, container events)
and matches them against rules expressed in YAML. The five rules below
are a tight starter set for new clusters. Most teams should also keep
the Falco default ruleset enabled and layer custom rules on top.

## 1. Shell spawned in a container

```yaml
- rule: Shell Spawned In Container
  desc: A shell process started inside a container; usually indicates
        an attacker pivoting or an operator running `kubectl exec`.
  condition: >
    spawned_process and container and shell_procs
    and not user_known_shell_spawn_activities
  output: >
    Shell spawned in container
    (user=%user.name container_id=%container.id image=%container.image.repository
     proc=%proc.cmdline parent=%proc.pname)
  priority: NOTICE
  tags: [container, shell, mitre_execution]
```

## 2. Write below /etc

```yaml
- rule: Write Below /etc
  desc: A process wrote to a path beneath /etc inside a container.
        /etc should be immutable in a hardened container; writes
        suggest configuration tampering.
  condition: >
    open_write and container
    and fd.name startswith /etc
    and not proc.name in (known_etc_writers)
  output: >
    Write below /etc
    (user=%user.name container_id=%container.id image=%container.image.repository
     proc=%proc.cmdline file=%fd.name)
  priority: WARNING
  tags: [filesystem, container, mitre_persistence]
```

## 3. Sensitive host path mounted

```yaml
- rule: Sensitive Host Path Mounted
  desc: A container mounted a sensitive host path (docker.sock,
        kubelet client config, kernel module dir, /proc). These mounts
        can lead to container escape or full node compromise.
  condition: >
    container.mount.dest in (sensitive_mount_destinations)
    and evt.type = container
    and evt.dir = >
  output: >
    Sensitive host path mounted
    (container_id=%container.id image=%container.image.repository
     mount=%container.mount.dest source=%container.mount.source)
  priority: CRITICAL
  tags: [container, mount, mitre_privilege_escalation]
```

Add to `lists` in the same Falco config:

```yaml
- list: sensitive_mount_destinations
  items:
    - /var/run/docker.sock
    - /var/lib/kubelet
    - /var/lib/kubelet/pki
    - /etc/kubernetes/admin.conf
    - /etc/kubernetes/pki
    - /root/.kube/config
    - /sys/module
    - /proc
```

## 4. Unexpected outbound network connection

```yaml
- rule: Unexpected Outbound Connection From Container
  desc: A container made an outbound connection to a destination not
        on the approved egress allowlist. Pair with NetworkPolicy for
        prevention; this rule provides detection.
  condition: >
    outbound and container
    and not fd.sip in (approved_egress_ips)
    and not fd.sport in (approved_egress_ports)
  output: >
    Outbound connection from container to unapproved destination
    (container_id=%container.id image=%container.image.repository
     dest=%fd.sip:%fd.sport proc=%proc.cmdline)
  priority: WARNING
  tags: [network, container, mitre_exfiltration]
```

## 5. Modify a binary file

```yaml
- rule: Modify Binary File
  desc: A process modified a binary file under a sensitive directory.
        Suggests post-exploitation persistence (planting a backdoor).
  condition: >
    bin_dir = /bin /sbin /usr/bin /usr/sbin /usr/local/bin
    and open_write
    and fd.directory in (bin_dir)
    and not proc.name in (known_package_managers)
  output: >
    Modify binary file
    (user=%user.name container_id=%container.id
     image=%container.image.repository file=%fd.name
     proc=%proc.cmdline parent=%proc.pname)
  priority: CRITICAL
  tags: [filesystem, persistence, mitre_persistence]
```

## Apply

```bash
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm install falco falcosecurity/falco \
  --namespace falco --create-namespace \
  --set falcosidekick.enabled=true \
  --set falcosidekick.config.slack.webhookurl=$SLACK_WEBHOOK
```

Custom rules go in `customRules:` of the chart values, or in a
ConfigMap mounted at `/etc/falco/rules.d/`.

## Test

```bash
kubectl run -it --rm shell-test --image=busybox -- sh
# Triggers "Shell Spawned In Container" rule.
```

## Tuning

Expect noise for the first week: `known_shell_spawn_activities`,
`known_etc_writers`, and `approved_egress_ips` lists need real data.
Iterate before turning on PagerDuty alerts.

## References

- Falco: <https://falco.org/docs/>
- Falco rule reference: <https://falco.org/docs/rules/>
- Falco rule library: <https://github.com/falcosecurity/rules>
- MITRE ATT&CK for Containers: <https://attack.mitre.org/matrices/enterprise/containers/>
