import sys;
import libvirt;

class VirtManager:
    def __init__(self):
        self._conn = None;
        self.open();

    def __del__(self):
        self.close();

    def open(self):
        try:
            self._conn = libvirt.open("qemu:///system");
        except libvirt.libvirtError as e:
            self._conn = None;
            print(repr(e), file=sys.stderr);

    def close(self):
        try:
            if self._conn != None:
                self._conn.close();
        except libvirt.libvirtError:
            # ignore closing errors
            pass;
        finally:
            self._conn = None;

    def getDomainsSorted(self) -> list[dict]:
        """
        Receives a list of all available domains.
        Domains are sorted by name.
        Active domains are listed first, then inactive.
        """

        if self._conn == None:
            return [];

        domains = self._conn.listAllDomains();
        def sortByActive(active: int) -> int:
            if active == 0: return 1;
            if active == 1: return 0;
        domains.sort(key=lambda domain: (sortByActive(domain.isActive()), domain.name()));

        fmtDomains = [];
        def activeAsBool(active: int) -> bool:
            if active == 0: return False;
            if active == 1: return True;
        for domain in domains:
            fmtDomains.append({
                "active": activeAsBool(domain.isActive()),
                "name": domain.name(),
                "uuid": domain.UUIDString(),
                #"domain": domain,
            });
        return fmtDomains;

    def bootVM(self, uuid: str, pretend: bool = True) -> bool:
        if self._conn == None:
            return False;

        try:
            domain = self._conn.lookupByUUIDString(uuid);
            if pretend:
                print("bootVM called");
            else:
                domain.create();
            return True;
        except libvirt.libvirtError as e:
            print(repr(e), file=sys.stderr);
            return False;

    def shutdownVM(self, uuid: str, pretend: bool = True) -> bool:
        if self._conn == None:
            return False;

        try:
            domain = self._conn.lookupByUUIDString(uuid);
            if pretend:
                print("shutdownVM called");
            else:
                domain.shutdown();
            return True;
        except libvirt.libvirtError as e:
            print(repr(e), file=sys.stderr);
            return False;
