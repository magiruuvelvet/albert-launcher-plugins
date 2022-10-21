import os;
import keyring;
from getpass import getpass;

import out.lib.libotpgenpy as otpgen;

path = f"{os.getenv('HOME')}/.config/マギルゥーベルベット/OTPGen/database";

#password = getpass("> ");
password = keyring.get_password("OTPGen", "secret");

otpgen.setTokenFile(path);
otpgen.setPassword(password);

if otpgen.loadTokens() != 0:
    exit(1);

tokens = otpgen.getTokens();
for token in tokens:
    print(token["index"], token["label"], len(token["icon"]));

query = "github";
res = [res for res in tokens if query.lower() in res["label"].lower()];
print(res);
