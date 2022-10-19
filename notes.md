# Source

Sourced from http://imode.gitlab.io/projects/c2/index.html

# Notes on WikiWikiWeb markup

whitespace lines break up paragraphs, not newlines

bracketing items, like ''' and '', do not apply across linebreaks, so

```
''this is italic''
```

but

```
''this is
not''
```

ISBNs dont seem to actually link to things

within a paragraph, there are only WikiWords, italics, bolds

italics and bolds are the only bracketting items. lists are higher-level inferred structures like in markdown

## '' and ''' interactions

This

```
''Foo '''''bar''''' baz.''
```

Renders as:

```html
<i>Foo </i><b>bar</b><i> baz.</i>
```

This:

```
'''''Foo''' bar '''baz.'''''
```

Renders as:

```html
<i><b>Foo</b> bar <b>baz.</b></i>
```

This:

```
''' ''Foo''''''
```

Renders as:

```html
<b> <i>Foo</i></b>
```

This:

```
'''Foo'''''bar'''''baz.'''
```

Renders as:

```html
<b>Foo</b><i>bar</i><b>baz.</b>
```

## rough rules, in order

```
WikiWords -> [WikiWords](/entries/WikiWords)
''''''    ->
'''       -> **
''        -> *
\t :\t    -> >
\tFoo:\t  -> Foo\n:
*^n       -> ( )^(n-1)-
(  )...   -> ```...```
\t1.?     -> 1.
```

## TextFormattingRules from c2wiki

For some examples of how these rules are used, see TextFormattingExamples.
To experiment with these rules, please try editing the WikiWikiSandbox. Please, do not experiment with this page because that is extraordinarily bad form.
Paragraphs
Do not indent paragraphs.
Words wrap to window width and fill as needed. (Emphasis fails to work if you insert end of line by hand!)
Use blank lines as separators.
Horizontal Lines
Four or more hyphens (----) at the beginning of a line make a horizontal rule.
Lists
asterisk in column one for bullet item
use more asterisks for deeper indenting
old format using tabs and numbered lists (lines starting with <tab(s)>number) is discouraged because of on-going problems some people have with tabs in browsers in general.
Fonts
Indent with one or more spaces to use a monospace font:
 This is text in a monospaced font indented with a space.
	This is indented with a tab stop.
This is not.
You can generate vertical whitespace by using multiple newlines after a monospaced line, but doing so to create more than one blank line is discouraged.
Indented Paragraphs (Quotes)
tab space colon tab -- often used (with emphasis) for quotations. (See SimulatingQuoteBlocks)
Sample:
This is quoted. (When a quoted line wraps, it too is indented maintaining an indented block.) If the text continues for a bit then the feature will be demonstrated nicely. You will see that each successive line is indented.
This isn't.
If you are going to ConvertSpacesToTabs, you need to type nine spaces, a colon, and then three spaces before the text. (See SimulatingQuoteBlocks.)
Definitions
Indented paragraphs are actually a special case of definitions. For example, to define a gnu, we would use
tab Gnu colon tab -- and then the definition. This looks like this:
Gnu
A furry animal.
You may use bold (see next paragraph), then it looks like this:
Gnu
A furry animal.
Emphasis
Use doubled single-quotes for emphasis (usually italics)
Use tripled single-quotes for strong emphasis (usually bold)
Use five single-quotes, or triples within doubles, for some other kind of emphasis (Bold Italic), but be careful about the bugs in the Wiki emphasis logic... (for example, text within doubled single-quotes followed immediately by text within tripled single-quotes is processed incorrectly)doubletriple Q:has this bug been fixed? No, but the overlapped tags produced are accepted by some browsers.
Emphasis can be used multiple times within a line, but cannot span across line boundaries.
Is there a simple way to do strike-throughs? perhaps ---three hyphens before and after--- ala ' ' ' for bold? [MichaelMuller 9/22/2004] NotOnThisWiki
Links
JoinCapitalizedWords to make links to Wiki pages.
Use SixSingleQuotes to separate capitalized prefixes (like 'Prefixed') from PrefixedWikiName, or to AvoidMakingLinksToWikiName, or to separate suffixes (like 's') from WikiNames. Put the six quotes after the prefix and before the first capitalized letter of the PrefixedWikiName (for example NonWikiName equals Non ' ' ' ' ' ' WikiName), or before a lowercase letter to avoid links in the entire word (for example AvoidMakingLinksToWikiName equals A ' ' ' ' ' ' voidMakingLinksToWikiName), or after the WikiName and before the suffix (for example WikiNames equals WikiName ' ' ' ' ' ' s).
Precede URLs with "http:", "ftp:", "gopher:", "mailto:", or "news:" to create links automatically as in: http://www.c2.com/. For a url containing an apostrophe, use %27 instead of the apostrophe.
URLs ending with .gif, .jpg, .jpeg or .png are inlined. (URLs ending with .jpe should be handled the same way, but aren't.) Note This approach means that image URLs with query parameters will not render as an image unless you add an extra "dummy" parameter ending with .gif, .jpg, .jpeg or .png at the end. Thankfully the need for such tricks is rare. (Bug: those image extensions must be lower-case).
Links to books specified by ISBN are treated specially. E.g., ISBN 0-13-748310-4 links to a bookseller. (The pattern is: "ISBN", optional colon, space, ten digits with optional hyphens, the whole thing optionally in square brackets. The last digit can be an "X".) We are an AmazonAssociate.
[1], [2], [3], [4] used to refer to remote links. This feature has been removed. See FixingLinks if you stumble across one of them.
VideoLink: Links to YouTube videos are translated to imbed codes. The video will show as a key frame with a play button in the center.
AnswerMe: Would it be possible to provide the same thing for other materials using ASIN instead of ISBN? -- AalbertTorsius [Linking to what? Amazon doesn't have many such materials.] [Just about anything that's not a book, right? Such as B000060PEU is http://www.amazon.com/exec/obidos/ASIN/B000060PEU (a Wacom drawing tablet) - and amazon certainly sells a lot of things that aren't books.][This could also be useful to link to scientific papers online via http://dx.doi.org followed by a number such as 10.1038/1011 which provides a unique and stable link to the article (e.g. http://dx.doi.org/10.1038/1011) and works for all publishers (Nope. It's not a stable link. This is a BrokenLink. 2005-09-19)]
WikiCase is needed to link to a single word [WikiSingleWordProblem]
Wiki has no syntax for an anchor point within a Wiki page; WikiWikiWebFaq explains why.
Wiki's TextFormattingRules aren't HTML
HTML tags don't work
&, <, and > are themselves
WhyDoesntWikiDoHtml?
Notes
When a rule says "tab," it wants a tab character without extra spaces around it. See TipForTypingTab if you have trouble entering tabs.
The actual TextFormattingRegularExpressions that implement these rules are available for those who can read them.
I've been able to see what's going on by opening the edit window as a new window in the browser. That way, I can link (in my mind) the text formatting rules with what finally gets displayed. Not that the rules are difficult!
Inserting lines with the LynxBrowser presents a special challenge. For help with that, see UsingWikiWithLynx.
Use italics sparingly when possible, as it's harder to read (especially at low resolution) than non-italics.

## TextFormattingRegularExpressions from c2wiki

This page complemented TextFormattingRules by exposing the exact regular expressions used by Ward's wiki when it was founded. If you do not find these useful, you can also consult TheWikiWay or any number of open source wiki implementations for alternatives.
Ah! That puts a different light on this page.
We look for paragraph boundaries...
	/^\s*$/  
(the expression matches empty lines and lines containing only whitespace (we don't look for the paragraph as a whole because the formatting script parses the text line-by-line))
definition, unordered and ordered lists...
	/^(\t+)(.+):\t/
(matches lines beginning with one or more tabs, followed by one or more characters, a colon, and a tab. The line in question does not have to be tab-final, and usually isn't)
	/^(\t+)\*/
	/^(\t+)\d+\.?/

preformatted text...
	/^\s/
(matches lines beginning with a whitespace character)
emphasis...
	/'{3}(.*?)'{3}/
	/'{2}(.*?)'{2}/
horizontal rules...
	/-{4,}/
external and internal links...
	/\[(\d)\]/
	/[A-Z][a-z]+([A-Z][a-z]+)+/
in-place hyperlinks...
	/\b((http)|(ftp)|(mailto)|(news)):[^\s\&lt\&gt\[\]"'\(\)]*[^\s\&lt\&gt\[\]"'\(\)\,\.]/
the search field macro...
	/\[Search\]/
characters that could mess up our html... (what about ampersand & &amp; ?)
	/&lt;/
	/&gt;/
and, when asked, spans of spaces to become tabs ...
	/ {3,8}/
The HTML specs say "In SGML, it is possible to eliminate the final ";" after a character reference in some cases .... We strongly suggest using the ";" in all cases to avoid problems with user agents that require this character to be present." http://www.w3.org/TR/html4/charset.html#entities
The specs also say that an ampersand which is not followed by an alphanumeric is to be displayed as is. -- PLA [[Cite? I can't find evidence to support this -- Danil]]
So, in fact, /&[^;]+\(\b[^;]\|$\)/, if I've not forgotten my perl, needs to be trapped and fixed. Then again, the patterns given genuinely recognize text which 'could mess up our html', which is what was stipulated - the dodgy texts matched don't need to be valid to serve as sentinels for trouble ... -- Eddy.
The HTML::Entity module neatly sidesteps the issue by doing all the hard work for you. If you like modules, that is. -- Paul
Java ORO BUG: If anyone is using jakarta ORO to hack a java-based Wiki, beware of that it doesn't handle the in-place hyperlinks regexp as expected. Replace it with something like this instead:
	/\b((http:)|(ftp:)|(mailto:)|(news:))[^\s\<\>\[\]"'\(\)]*[^\s\<\>\[\]"'\(\)\,\.]/
-- NiclasOlofsson
Could somebody please point me to the right way of handling external links that contain a wikiword?
Currently, I replace all
 (http|news|ftp|mailto)\:(\/\/)?((?:\S(?!\.gif|\.jpg|\.jpeg))+)\s
with
 <a href="$1:$2$3">$3</a>
but if the url is, for example, http://c2.com/cgi/wiki?WikiPage, the link gets garbled later by my wikiword replacement like this
 (\b[A-Z][a-z]+[A-Z][A-Za-z]*\b)
with
 <a href="/$1">$1</a>
Could somebody please point me to a solution? Thanks. -- SvenNeumann
Before processing raw page text QuickiWiki extracts links, stores them in a list, and replaces each with a placeholder. Once text formatting is done, it restores the links, removing the placeholders. You can also use this technique to implement literal text (e.g., code blocks).
SvenNeumann, if you define a WikiWord as:
/(\s)([A-Z][a-z]+[A-Z][A-Za-z]*)/
and replace it with the captured beginning whitespace, it seems to work fine, and avoids wikiWordsWithinWordsAndurls. it does have the adverse effect of .WikiWord not being a WikiWord.
-- DanielStaudigel
Hi DanielStaudigel. Why exactly do I want to capture whitespace at the beginning? a WikiWord might not have white space before (but punctuation instead). --SvenNeumann
Implementations I have seen replace all URLs temporarily with some implausible-to-type combination of ASCII characters, do the WikiWord substitution, then put the URLs, with HTML, back in. (An alternative is to use an excessively complex Perl regex that handles WikiWords and URLs simultaneously using executed substitutions or some such. Or just use m/\G ... /gc) -- Chris Purcell (KritTer)
I.e. using regular expressions in the context of text formatting. Some such things are trivial, others are deceptively slippery.
This page could have been really, genuinely useful to my endeavors the last two days and I was very happy when I found it. Unfortunately, I must say I find many of the expressions here dodgy at best, and just wrong at worst. Could we turn this into a resource for the (many) ways that WikiAuthors have implemented this? -- SvenNeumann
See influential RobPike paper on StructuralRegularExpressions, though that does not appear to be the idea of this page.
