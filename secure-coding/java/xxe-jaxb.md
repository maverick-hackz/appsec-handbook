# XML External Entity (XXE) in JAXB / DocumentBuilder / SAX

## Threat

An XML parser that resolves external entities or DTDs reads attacker-chosen
files, performs SSRF, or hangs on billion-laughs amplification. JDK XML
factories default to permissive behaviour for backward compatibility;
hardening is the caller's responsibility.

CWE: CWE-611 (Improper Restriction of XML External Entity Reference),
CWE-776 (Improper Restriction of Recursive Entity References).

## Insecure

```java
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
DocumentBuilder db = dbf.newDocumentBuilder();
Document doc = db.parse(request.getInputStream());

JAXBContext ctx = JAXBContext.newInstance(Order.class);
Order o = (Order) ctx.createUnmarshaller()
        .unmarshal(request.getInputStream());

TransformerFactory tf = TransformerFactory.newInstance();
Transformer t = tf.newTransformer(new StreamSource(...));
```

## Why it fails

- Defaults resolve external DTDs and entities. `<!DOCTYPE foo [
  <!ENTITY x SYSTEM "file:///etc/passwd"> ]>` returns the file's contents
  to the caller, an internal HTTP endpoint, or stdout.
- JAXB and StAX implementations share the same risk; harden each factory.

## Secure

```java
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
dbf.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
dbf.setXIncludeAware(false);
dbf.setExpandEntityReferences(false);
DocumentBuilder db = dbf.newDocumentBuilder();
```

```java
SAXParserFactory spf = SAXParserFactory.newInstance();
spf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
spf.setFeature("http://xml.org/sax/features/external-general-entities", false);
spf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
SAXParser sax = spf.newSAXParser();
```

```java
TransformerFactory tf = TransformerFactory.newInstance();
tf.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);
tf.setAttribute(XMLConstants.ACCESS_EXTERNAL_DTD, "");
tf.setAttribute(XMLConstants.ACCESS_EXTERNAL_STYLESHEET, "");
```

For JAXB, prefer feeding the parsed DOM (with the hardened factory above)
into the unmarshaller, rather than passing raw streams:

```java
JAXBContext ctx = JAXBContext.newInstance(Order.class);
Order o = (Order) ctx.createUnmarshaller().unmarshal(hardenedDocument);
```

## Notes

- `FEATURE_SECURE_PROCESSING` alone is necessary but not sufficient on
  some JDK / Xerces combinations; set the explicit feature names too.
- For high-volume parsing, set entity-expansion limits via
  `System.setProperty("jdk.xml.entityExpansionLimit", "0")` (deny) or a
  small numeric ceiling.
- If the application does not need XML at all, do not accept it. Pin
  `Accept` and `Content-Type` to JSON in the controller layer.

## References

- OWASP XML External Entity Prevention Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html>
- CWE-611: <https://cwe.mitre.org/data/definitions/611.html>
- JDK XML processing (Java Tutorials): <https://docs.oracle.com/en/java/javase/17/docs/api/java.xml/module-summary.html>
