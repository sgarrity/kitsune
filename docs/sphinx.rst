.. _sphinx:

========================
Installing Sphinx Search
========================


Requirements
------------

* `Sphinx <http://www.sphinxsearch.com/>`_ 0.9.9


Overview
--------

Sphinx--the search engine, not the documentation engine--powers Kitsune's
search app. Sphinx has three parts: a server daemon, an indexer that runs
as a cronjob, and a client. In this case, the client is Kitsune, and we
wrap the Python port of the lower-level client (see ``sphinxapi.py``).

There are ports of the client to several languages--PHP is the reference
implementation, but there are also Python, Ruby, Java, C, and others.
These clients all use Sphinx's binary API, but there is also a SQL API,
which can use any MySQL client. Eventually we will probably write our own
lower-level client that operates over the SQL API, since performance scales
much better through the compiled MySQL clients.

The server and indexer are written in C. You shouldn't have to do more than
install and run those.


How it Works
~~~~~~~~~~~~

The Sphinx indexer takes documents from a "source" and turns them into an
"index". Both the source and the index are defined in a configuration file,
usually called ``sphinx.conf``. (You can see ours in the ``configs/``
directory.) "sources" can be either SQL queries or XML documents. We use
queries because it removes a level of complexity by not generating XML,
even though it makes the queries rather complex.

The "index" definitions are largely boiler-plate and concerned with what
characters are counted as "word" characters and what characters need
special, ideographic handling, like CJK. Don't worry much about that part.

If ``sphinx.conf`` is executable, Sphinx executes it and uses whatever it
prints to stdout as its configuration. We use that to allow string
interpolation of our database settings and keep ``sphinx.conf`` generic.

To use our ``sphinx.conf``, you'll need to set up a ``localsettings.py``
with database connection and file location information. There is a
``localsettings.py-dist`` you can copy.


Important Caveat
^^^^^^^^^^^^^^^^

``localsettings_django.py`` is important for tests, but will be ignored if
a ``localsettings.py`` exists in the same directory. You should copy the
``sphinx.conf`` file somewhere else and put your ``localsettings.py`` with
the copy. For example::

    $ mkdir ~/sphinx/
    $ cd /path/to/kitsune
    $ cp configs/sphinx/sphinx.conf ~/sphinx/
    $ cp configs/sphinx/localsettings.py-dist ~/sphinx/localsettings.py
    $ cd ~/sphinx/
    $ vim localsettings.py  # configure as necessary
    $ indexer -c sphinx.conf --all  # see below
    $ searchd -c sphinx.conf  # see below


Running Sphinx
--------------

The first step is to run the indexer the first time. Assuming you've
installed Sphinx, however you need to on your OS, and both ``indexer`` and
``searchd`` are in your path, you should only need to do::

    $ indexer -c /path/to/sphinx.conf --all

The ``-c`` option points to the configuration, and ``--all`` means "index
all the sources you find in the configuration." You can replace ``--all``
with specific index names (we have ``discussion_forums``, ``forum_threads``
and ``wiki_pages``) to only update one or two indexes.

The other important option for ``indexer`` is ``--rotate``, which allows
you to generate new indexes and replace the current ones while ``searchd``
is running. For example::

    $ indexer --rotate --all -c /path/to/sphinx.conf

Once you've created indexes the first time, you can start ``searchd``. It's
pretty straight forward::

    $ searchd -c /path/to/sphinx.conf

Now the Sphinx server is up and running. For more info on ``searchd``, just
try ``searchd --help``. Make sure that ``LISTEN_PORT`` in your
``localsettings.py`` matches ``SPHINX_PORT`` in ``settings.py`` and try
searching.


Testing with Sphinx
-------------------

To run the test suite, you may need to point ``SPHINX_INDEXER`` and
``SPHINX_SEARCHD`` at the correct ``indexer`` and ``searchd`` locations, if
they don't match the defaults in ``settings.py``.

Testing introduces an interesting complication: the test suite needs to run
its own copy of Sphinx. It reads settings from ``localsettings_django.py``,
and there are two obvious problems:

* Two instances of ``searchd`` cannot listen to the same port.

* Your personal ``searchd`` will not have the correct data for the tests.

So you have three options:

* Don't run your own ``searchd`` unless you're actually working on search.
  This is pretty easy: just don't start it.

* Run ``searchd`` on the same port, but shut it down to run the tests. Paul
  does this, but I think it mostly turns into option 1.

* Run ``searchd`` on a different port. This is what I do. I set the
  ``SPHINX_PORT`` in ``settings_local.py`` to the port of my ``searchd``
  instance, then comment it out when I'm not manually testing search.
  I hope to make this option more automatic by improving the test runner.
  IE: you could conditionally define settings in ``settings_local.py``
  only when you are *not* in a test-running environment.

Hopefully this problem will go away in the future.
