import ipaddress
import re


def _is_private_ipv4(ip: str) -> bool:
    try:
        ipobj = ipaddress.ip_address(ip)
        return ipobj.version == 4 and ipobj.is_private
    except ValueError:
        return False

def rewrite_sdp_candidates_for_vpn(sdp: str, new_ip: str, drop_srflx: bool = True, drop_ipv6: bool = True) -> str:
    out = []
    for line in sdp.splitlines():
        # 1) c-line -> VPN
        if line.startswith("c=IN IP4 "):
            out.append(f"c=IN IP4 {new_ip}")
            continue

        # 2) a=rtcp:... IN IP4 X -> VPN (если встречается)
        if line.startswith("a=rtcp:") and " IN IP4 " in line:
            out.append(re.sub(r"(a=rtcp:\d+\s+IN IP4\s+)[0-9.]+", rf"\g<1>{new_ip}", line))
            continue

        # 3) Кандидаты
        if line.startswith("a=candidate:"):
            parts = line.split()
            # формат: a=candidate:<foundation> <component> <transport> <priority> <ip> <port> typ <type> ...
            if len(parts) >= 8:
                ip = parts[4]
                cand_type = None
                for i in range(6, len(parts)-1):
                    if parts[i] == "typ":
                        cand_type = parts[i+1]
                        break

                # выкинуть srflx
                if drop_srflx and cand_type == "srflx":
                    continue

                # выкинуть IPv6
                if drop_ipv6 and ":" in ip:
                    continue

                # приватный IPv4 -> заменить на VPN
                if _is_private_ipv4(ip) and ip != new_ip:
                    parts[4] = new_ip

                line = " ".join(parts)

        out.append(line)

    return "\r\n".join(out) + "\r\n"
