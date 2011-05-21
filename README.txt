plone.phonehome Package Readme
====================================

Overview
--------

This package provides anonymous usage staticstics 

A check-in call is made during Zope startup. If the list of installed packages
has changed since the previous check-in, that list of packages will be
submitted.

Installation
------------
To install ``plone.phonehome``, add it to the ``eggs`` list in your
``buildout.cfg``. ZCML configuration will be automatically loaded via a
``z3c.autoinclude`` entry point.

Querying
--------

The ``http://plonephonehome.appspot.com`` application provides a ``query``
method which will return the number of reported instances using the provided
``package`` and ``version``. A ``query`` call might look something like:

    http://plonephonehome.appspot.com/query?package=Products.CMFPlone&version=4.0

