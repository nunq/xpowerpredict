# xrankpowerpredict

i was inspired by [snowpoke's](https://www.twitch.tv/snowpoke) prediction system and wanted to do some predicting myself.

beware, it's ugly python code.

## setup

> thanks to good ol' ninty, this is hella complicated.

we need the `iksm_session` token that the nintendo switch online app uses for auth, etc.

> how do i get that token?

[here's a guide](https://github.com/frozenpandaman/splatnet2statink/wiki/mitmproxy-instructions). beware that if you try this on android, you'll need an android version below 7.0 (nougat), because later versions have a different policy for user-imported certificates.

if you're lucky (like me), you have an old phone with android 6.0 (marshmellow) lying around, otherwise you'd need to screw around with android virtual machines (probably not that fun tbh).


## how do i run this?

first, adjust the config options in the script.

then do `python3 [path to script]` before the match starts. hit 'refresh' some time after the lobby screen says 'BATTLE TIME!'. 

happy _VEEEEMO_

## how does this work

magic, obviously.

... jk. as soon as a match starts your xpower (in the app) is updated to the value that i'd be if you lost the match.
using _math_ and other _magic_ we can - somewhat accurately - estimate the points you'd gain. i got the formulas by messing around in google sheets with some test data.


## etc

license: gpl3

