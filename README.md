# Tree Tagger Instration

1. Download the tagger package for your system (PC-Linux, Mac OS-X, ARM-Linux).

  ex) for Linux

      mkdir treetagger
      cd treetagger
      wget http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tree-tagger-linux-3.2.1.tar.gz

1. Download the tagging scripts into the same directory.

        wget http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tagger-scripts.tar.gz

1. Download the installation script install-tagger.sh.

        wget http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/install-tagger.sh

1. Download the parameter files for the languages you want to process.

  ex) for English

      http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/english-par-linux-3.2-utf8.bin.gz

1. Open a terminal window and run the installation script in the directory where you have downloaded the files:

        sh install-tagger.sh

1. Make a test, e.g.

        echo 'Hello world!' | cmd/tree-tagger-english 

    or 

        echo 'Das ist ein Test.' | cmd/tagger-chunker-german

## Tree Tagger Site
http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/

# Python Dependency
1. Tree Tagger Wapper

        pip install treetaggerwrapper

2. Mongo DB

        sudo apt-get install -y mongodb-org
        pip install pymongo

3. Word Cloud

        git clone https://github.com/amueller/word_cloud
        cd word_cloud/
        pip install .

4. Matplotlib

        sudo apt-get build-dep python3-matplotlib
        sudo apt-get install -y fonts-migmix
        pip install matplotlib
