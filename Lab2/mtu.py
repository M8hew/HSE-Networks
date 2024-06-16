import subprocess
import argparse

class MinMTU:
    def __init__(self, host: str):
        self.host = host
        self._min_pos = 0
        self._max_pos = 120000

    def check_mtu_packet_size(self, packet_size, timeout=50) -> bool:
        p = subprocess.Popen(
            f'ping -M do -c 1 -s {packet_size} {self.host}',
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
        )

        for line in iter(p.stdout.readline, b''):
            line = line.decode(encoding='utf-8')
            if 'packet size too large' in line:
                return False
            if 'Message too long' in line:
                return False
            if '100.0% packet loss' in line:
                return False
            
        print(f"* New iteration: trying packet_size {packet_size}")
        code = p.wait()
        return code == 0

    def find_min_mtu(self):
        print('Running:')
        
        while self._max_pos - self._min_pos - 1 > 0:
            mid = self._max_pos + self._min_pos
            mid //= 2
            if self.check_mtu_packet_size(mid):
                self._min_pos = mid
            else:
                self._max_pos = mid
        
        return self._min_pos


def main():
    parser = argparse.ArgumentParser(description='Find minimum MTU.')
    parser.add_argument('--host', required=True, type=str, help='Host URL')
    args = parser.parse_args()

    f = MinMTU(args.host)
    result = f.find_min_mtu()
    print("Done")
    print(f"min MTU: {result} bytes [without headers]")

if __name__ == "__main__":
   main()