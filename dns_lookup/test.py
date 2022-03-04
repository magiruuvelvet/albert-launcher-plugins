import dns.resolver;

try:
    result = dns.resolver.resolve("magiruuvelvet.gdn", "A");
    for val in result:
        print(val.to_text());
except dns.resolver.NoAnswer:
    print("NoAnswer");
except dns.resolver.NXDOMAIN:
    print("NXDOMAIN");
except dns.rdatatype.UnknownRdatatype:
    print("Invalid DNS Type");
