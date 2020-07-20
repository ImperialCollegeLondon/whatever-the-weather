# Whatever the Weather

Keen to take part in Advanced Hackspace's ["Whatever the Weather" Coding Challenge](https://mailchi.mp/48a7b9c1e543/hack-at-home-whatever-the-weather-coding-challenge) but unsure how to get started?

In this post we'll write a super-minimal Python app - without making things complicated.

We'll use an online weather service to check the forecast first thing in the morning and send you an email reminding you to take an umbrella if rain is on its way.

All you'll need is a Gmail login (though the program can easily be modified to use other email or notification services - see below), and a GitHub account (which you'll need to submit your entry anyway).

So first of all, Googling for weather APIs provides various options, including one from the [Norwegian Meteorological Institute](https://api.met.no/doc/). It turns out they provide free global forecasts, with no registration necessary. The first "Sample request URL" on their [Locationforecast](https://api.met.no/weatherapi/locationforecast/2.0/documentation) page looks promising, so let's plug in some coordinates for London and see what we get:

https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=51.5&lon=0

This gives us lots of data in [JSON](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON) format. A helpful thing to do is copy and paste the data into a [page that makes it easier to explore](https://www.jsonformatter.io). If you do that then you'll see some `timeseries` elements, each of which contain forecast information. If we take the first one we can get a prediction for the total precipitation over the next 6 hours. If it's greater than zero then that's hopefully a good indication that we'll need an umbrella.

So how do we do this in Python? Well, if we break it down it's really just three steps:

1. Retrieve the JSON and extract the predicted precipitation
2. Check whether it's greater than zero
3. If so then send an email

Fortunately all this functionality is built into Python, and we end up with a [short script](https://github.com/ImperialCollegeLondon/whatever-the-weather/blob/main/main.py). On macOS it can be run as follows:

```sh
python3 main.py
```

You'll be prompted for your Gmail address (e.g. john.smith@gmail.com) and password. The only tricky thing here is that because we're sending ourselves an email we set the "From" and "To" addresses to be the same (which is also our Gmail login). If you're using two-factor authentication (2FA) for your Google account (and you probably should be...) then you'll need to create an [App Password](https://support.google.com/accounts/answer/185833?hl=en). If you're not using 2FA then you may need to enable [less secure apps](https://support.google.com/accounts/answer/6010255?hl=en). Either way, you should be very careful about how keeping your password safe: be sure not to embed any credentials in your script! If you don't have a Gmail account or would rather not use your credentials then there are many third-party SMTP services that have a free tier (e.g. [SendGrid](https://sendgrid.com/docs/for-developers/sending-email/integrating-with-the-smtp-api/)).

So, we have a working script but how can we automate its execution? Well [GitHub Actions](https://docs.github.com/en/actions) can help here, thanks to its [workflow scheduling](https://docs.github.com/en/actions/reference/events-that-trigger-workflows#schedule) feature. All just need to upload our `main.py` file to a new GitHub repository, ensure that we store our email address and password securely [in a secret](https://docs.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets), and then create [a minimal workflow](https://github.com/ImperialCollegeLondon/whatever-the-weather/blob/main/.github/workflows/main.yml) that [triggers our script at 06:00 UTC on weekdays](https://crontab.guru/#0_6_*_*_1-5).

And there we have it: thanks to a couple of short scripts and some free services we'll never forget our umbrella again! If you just fork [our repository](https://github.com/ImperialCollegeLondon/whatever-the-weather) and set `EMAIL` and `PASSWORD` as secrets then you'll start getting notifications. But this is just the start... perhaps you can integrate this script with some fancier notification methods such as Slack or SMS using [IFFFT](https://ifttt.com/)? Run it on a Raspberry PI or [hook it up to any smart devices](https://www.home-assistant.io/) in your home? Build a simple desktop app using [BitBar](https://getbitbar.com), perhaps with a forecast for your actual location by using a [geolocation API](http://ip-api.com/json/) to retrieve your latitude and longitude?

Whatever you do, good luck with Hacking at Home - we can't wait to see what you create!

_Short courses in Software Engineering and many other topics are available via the Graduate School's [Research Computing & Data Science](https://www.imperial.ac.uk/study/pg/graduate-school/students/doctoral/professional-development/research-computing-data-science/courses/) programme._
