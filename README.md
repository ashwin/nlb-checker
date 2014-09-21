NLB Checker
===========

A simple Python script to check which of the books you want are available
for borrowing right now at your neighborhood [NLB Singapore](http://nlb.gov.sg/)
libraries.

This was created to scratch a personal itch. I keep a list of books I want to
read and I visit my neighborhood library every weekend. Before leaving home, I
want to check which of the books I want are available for borrowing. To do that
using the NLB website, I would have to check manually for *every single book*.
That is painful if your to-read book list is huge! :-)

Usage
=====

1. For every book you want to borrow, find its BRN ID. You can find this field
   in the NLB webpage for the book.

2. Add the BRN IDs to a text file, one per line. Assume this file is books.txt

3. Add the name of the libraries where you want to check to a file. Assume
   this file is libs.txt

4. To see which of the books in books.txt are available in the libraries in
   libs.txt, invoke the script as:

```
$ ./nlb-checker.py --books-path books.txt --libs-path libs.txt
```

License
=======

This script is shared under the [MIT License](http://opensource.org/licenses/mit-license.php).
