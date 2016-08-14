# Kanji Sentences
Kanji Sentences is a simple addon for Anki allowing a user to suspend or unsuspend Japanese flashcards based on whether or not you have seen a particular kanji.

Currently, the functionality is quite limited - it will simply check the "Kanji" (case insensitive) field of all existing flashcards that are not in the new state (seen at least once) and consider these kanji as being "known". Then, depending on the menu option you choose, it will suspend sentences with unknown kanji or unsuspend sentences without unknown kanji.

Kanji Sentences is available on Github:

https://github.com/ChrisPWill/AnkiKanjiSentences

Some code was inspired from the modified version of Kanji Grid, which I also recommend:

https://ankiweb.net/shared/info/942570791

### Installation
Copy kanjisentences.py into your Anki plugins directory

### Planned features
- A configuration menu allowing operations to be run only on certain decks and fields
- Ability to bury instead of suspend

### Development
Want to contribute? Great! Any code contributions are very welcome. If it's a feature that might take some time, do submit an issue on the issue tracker so that someone else doesn't try to do the same thing. I will also post to the issue tracker when I begin work on a new feature that will take me more than a single coding session.

