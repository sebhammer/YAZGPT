# YAZGPT - an experimental bibliographic chatbot
Copyright (c) 2023 Sebastian Hammer, see LICENSE file for details   

The purpose of this little project is to build a basic platform
where I can experiment with the ability of an LLM to generate queries,
issue searches against a bibliographic database, and
interpret the results. The idea is to use a chatbot as a way to quickly
explore and prototype prompts and models that might support different types
of library applications like cataloging, collection analysis, resource sharing, etc.

I'm incredibly rusty as a developer and know no
Python, so please don't judge.

**Caveat**

In its present form, this is not meant tobe a useful tool for any specific use case -- it is just
intended as a fun way
to explore whether generative API can have a role in bibliographic data flows. The
present version is hardwired to search the Libray of Congress.

**Prerequisites**

YAZGPT.py needs to zee "zoomsh" in its path.
Zoomsh is part of the
[YAZ toolkit](https://www.indexdata.com/resources/software/yaz). You can easily
find it for almost any platform. I run this on a Mac.

You need an OpenAI API key. The code looks for it in the
OPENAI_API_KEY environment variable.

**Synopsis**

```
python3 YAZGPT.py --help     # for an overview of command-line options and parameters
```

**Example sessions**

```
Welcome to the YAZGPT AI-powered Z39.50 client

YAZGPT>> find publications by Robert Pirsig, combine the results by title and list
          editions under each title
                                                               
Function Call search {
  "author": "Pirsig, Robert"
}
Hitcount:  11
Here are the publications by Robert Pirsig, grouped by title and listed with their editions:

1. Title: John Dewey, Robert Pirsig, and the art of living
   - Edition 1: New York: Palgrave Macmillan, 2006

2. Title: Lila
   - Edition 1: New York: Bantam Books, 1991
   - Edition 2: New York, N.Y.: Bantam Audio, p1991 (Contributor: Will Patton)

3. Title: On quality
   - Edition 1: Boston: Mariner Books, [2022] (Editor: Wendy K. Pirsig)

4. Title: Zen and the art of motorcycle maintenance
   - Edition 1: New York: W. Morrow, 1999
   - Edition 2: New York: Morrow, 1974
   - Edition 3: New York: Quill, 1999
   - Edition 4: New York: Morrow, 1984, c1974
   - Edition 5: Los Angeles, CA: Audio Renaissance ; p1999 (Contributor: Lawrence Pressman)

5. Title: Zen and now
   - Edition 1: New York: Alfred A. Knopf, 2008

Please note that "Lila" and "Zen and the art of motorcycle maintenance" have multiple editions.

YAZGPT>> 

```
Here is a fun recursive example -- note, lots of tuning and tweaking needed to make this operational, but
a really interesting example of the AI using the output of one search to launch another.

```
YAZGPT>> find the book with isbn 0688002307, then use a title/author search to locate
            potential matching editions. Make a list of only those results where the
            Author and Title are similar to the original book
     
Function Call search {
  "isbn": "0688002307"
}
Hitcount:  1
Function Call search {
  "title": "Zen and the art of motorcycle maintenance:",
  "author": "Pirsig, Robert M."
}
Hitcount:  7
Here are the potential matching editions of the book "Zen and the art of motorcycle maintenance" by
   Robert M. Pirsig that have similar titles and authors:

1. Title: Zen and the art of motorcycle maintenance:
   - Author: Robert M. Pirsig
   - Publication: New York, Morrow, 1974.
   - ISBN: 0688002307

2. Title: Zen and the art of motorcycle maintenance :
   - Author: Robert M. Pirsig
   - Publication: New York, W. Morrow, 1999.
   - ISBN: 0688171664 (pbk.)

3. Title: Zen and the art of motorcycle maintenance :
   - Author: Robert M. Pirsig
   - Publication: New York, Morrow, 1984, c1974.
   - ISBN: 0688032079

Please note that these are the editions that have similar titles and authors to the original
   book. If you need more information about any of these editions, please let me know.

YAZGPT>> 


```

**TODO**

Explore use cases and sumarize results: General research, copy cataloging, resource sharing

Refine the mapping of records. Is it possible to give access to additional fields/detailed records
on demand? I'm thinking about an option to return full MARC for small result sets, with an error message back if
too many records are returned.

Would it make sense to predefine multiple search targets and let the LLM choose the modst appropriate one? Create
etc/targets and a way to specify a list of available targets for a session.

List remaining context buffer space; add some kind of cleanout/compression of older messages. Right now, everything
is kept which is likely to lead to crummy results is a session goes on too long anyway.

Make the temperature a command line setting to allow experimentation. Possibly, t=0 would be preferable for 
these kinds of explorations but right now the "creativity" of temp=1 may be good for discovery/ideation.
