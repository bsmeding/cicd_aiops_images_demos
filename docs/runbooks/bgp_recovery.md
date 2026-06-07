# BGP Recovery Runbook

## Symptoms

- BGP neighbor state is `Idle`, `Active`, or `Connect`
- Prefixes from a peer are missing from the routing table
- BGP session logs show repeated resets

## Diagnosis

1. Check peer reachability:
   ```
   ping <neighbor-ip> source <local-ip>
   ```
2. Verify BGP configuration:
   ```
   show ip bgp neighbors <neighbor-ip>
   ```
3. Check for authentication issues in logs:
   ```
   show logging | include BGP
   ```
4. Review received and advertised routes:
   ```
   show ip bgp neighbor <neighbor-ip> routes
   show ip bgp neighbor <neighbor-ip> advertised-routes
   ```

## Recovery steps

1. If the session is stuck, clear it:
   ```
   clear ip bgp <neighbor-ip> soft
   ```
2. If soft reset does not help:
   ```
   clear ip bgp <neighbor-ip>
   ```
3. Verify prefix limits are not exceeded:
   ```
   show ip bgp summary | include <neighbor-ip>
   ```
4. If the issue persists, check for route-map or prefix-list mismatches.

## Escalation

Escalate to network team if:
- Session cannot be established after 10 minutes
- Multiple peers are affected simultaneously
- BGP flap is correlated with a hardware or link event
