# Interface Troubleshooting Runbook

## Symptoms

- Interface shows `down/down` or `up/down` in `show interfaces`
- High error counters (input errors, CRC, output drops)
- Intermittent connectivity to directly connected device

## Diagnosis

1. Check interface status:
   ```
   show interfaces <interface>
   show interfaces <interface> counters errors
   ```
2. Verify physical layer:
   - Check SFP/cable seating
   - Verify speed and duplex settings match the far end
3. Check for CDP/LLDP neighbor:
   ```
   show cdp neighbors <interface> detail
   ```
4. Review recent syslog entries:
   ```
   show logging | include <interface>
   ```

## Recovery steps

1. Bounce the interface:
   ```
   interface <interface>
     shutdown
     no shutdown
   ```
2. If SFP-based: swap SFP module and test
3. If copper: test cable with a cable tester, try a known-good cable
4. If speed/duplex mismatch: set both ends to the same value:
   ```
   interface <interface>
     duplex full
     speed 1000
   ```
5. Clear error counters after fix:
   ```
   clear counters <interface>
   ```

## Escalation

- If the interface continues to flap after hardware replacement, escalate to vendor TAC
- Document error counter baseline before and after the fix
