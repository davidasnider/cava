# Purpose

This service listens to amcrest cameras, listening for motion events and
forwarding to cava.

## Debugging

Only one api connection is allowed at a time, it is therefore important when
debugging to scale our deployment to 0.

```bash
k config use-context k8s2
k scale deployment --replicas 0 sensor-amcrest-bedroom -n cava
```
