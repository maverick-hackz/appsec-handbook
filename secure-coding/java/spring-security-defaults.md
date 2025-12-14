# Spring Security 6 Defaults

## Threat

Spring Security ships secure defaults, but many production setups disable
them while debugging (`csrf.disable()`, permit-all rules added in haste)
and never re-enable. A few opinionated choices on top of the defaults
prevent the common authentication, CSRF, and header bugs.

CWE: CWE-352 (CSRF), CWE-693 (Protection Mechanism Failure), CWE-1004
(Sensitive Cookie Without HttpOnly), CWE-79 (XSS — partially mitigated by
headers).

## Insecure

```java
@Configuration
@EnableWebSecurity
class SecurityConfig {
    @Bean
    SecurityFilterChain chain(HttpSecurity http) throws Exception {
        http.csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(a -> a.anyRequest().permitAll())
            .formLogin(Customizer.withDefaults());
        return http.build();
    }
}
```

## Why it fails

- `csrf.disable()` on a cookie-authenticated browser application removes
  the only built-in CSRF defence.
- `permitAll()` on `anyRequest()` skips authorization even when
  `formLogin` is configured.
- Default `PasswordEncoder` from `User.withDefaultPasswordEncoder()` (a
  static factory used in some examples) embeds the algorithm in the hash
  with `{noop}` or `{bcrypt}` prefixes — easy to misuse.

## Secure

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
class SecurityConfig {

    @Bean
    SecurityFilterChain chain(HttpSecurity http) throws Exception {
        http
            // CSRF on for state-changing requests; explicit exceptions only.
            .csrf(csrf -> csrf
                .csrfTokenRequestHandler(new CsrfTokenRequestAttributeHandler())
                .ignoringRequestMatchers("/api/webhooks/**"))
            // Default-deny authorization.
            .authorizeHttpRequests(a -> a
                .requestMatchers("/", "/login", "/css/**", "/js/**").permitAll()
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated())
            // Session: rotate on login; invalidate on logout.
            .sessionManagement(s -> s
                .sessionFixation().changeSessionId()
                .maximumSessions(5).maxSessionsPreventsLogin(false))
            // Security headers via the default set + HSTS preload.
            .headers(h -> h
                .contentTypeOptions(Customizer.withDefaults())
                .frameOptions(f -> f.deny())
                .httpStrictTransportSecurity(hsts -> hsts
                    .includeSubDomains(true)
                    .maxAgeInSeconds(31536000))
                .referrerPolicy(r -> r.policy(
                    ReferrerPolicy.STRICT_ORIGIN_WHEN_CROSS_ORIGIN))
                .contentSecurityPolicy(csp -> csp
                    .policyDirectives("default-src 'self'; "
                                    + "object-src 'none'; "
                                    + "base-uri 'self'")))
            .formLogin(Customizer.withDefaults())
            .logout(l -> l.invalidateHttpSession(true).deleteCookies("JSESSIONID"));
        return http.build();
    }

    @Bean
    PasswordEncoder passwordEncoder() {
        // Spring Security delegating encoder defaults to bcrypt; switch
        // to Argon2id explicitly when the legacy data set is migrated.
        return PasswordEncoderFactories.createDelegatingPasswordEncoder();
    }
}
```

For REST APIs:

```java
http
    .csrf(AbstractHttpConfigurer::disable)    // bearer-token APIs, no cookies
    .sessionManagement(s -> s.sessionCreationPolicy(
            SessionCreationPolicy.STATELESS))
    .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
    .authorizeHttpRequests(a -> a.anyRequest().authenticated());
```

## Notes

- Disable CSRF only when the application is fully bearer-token-based AND
  cookies are not part of the auth surface. A mixed-cookie/bearer app
  needs CSRF for the cookie paths.
- Pin `Content-Security-Policy` to `'self'` plus a hash/nonce-allowlisted
  set of inline scripts; `unsafe-inline` defeats the policy.
- For method-level checks, `@PreAuthorize("hasRole('ADMIN')")` complements
  HttpSecurity but does NOT replace authorization on the data layer for
  object-level access.
- Spring Boot autoconfiguration enables `actuator` endpoints; lock them
  down with `management.endpoints.web.exposure.include` and a separate
  security filter chain on the management port.

## References

- Spring Security Reference (current GA): <https://docs.spring.io/spring-security/reference/>
- OWASP Spring Security Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Java_Security_Cheat_Sheet.html>
- Spring Security CSRF documentation: <https://docs.spring.io/spring-security/reference/servlet/exploits/csrf.html>
- OWASP Secure Headers Project: <https://owasp.org/www-project-secure-headers/>
