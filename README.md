# Don't Huff

Don't Huff is a barebones data logger for the wclh data loggers sold by various
vendors on Aliexpress.

# Requirements

Install the `pip` requirements, per `requirements.txt`:

```
pip install -r requirements.txt
```

You will need the wclh PM2.5/CO2/HCHO/RH&T/TVOC sensor. You can simply plug it
in, find the UART's device node, and then run the app.

This will then yield dicts of the contents of these messages. You can then do
as you see fit with those.

