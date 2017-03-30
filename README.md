## _anno-dbnsfp_

    Annotate non-synonymus SNPs with values found in [dbNSFP](https://sites.google.com/site/jpopgen/dbNSFP).
    
    ### Installation and usage for running on Simons Foundation/Flatiron Institute cluster. 

        [sqlite3](http://www.sqlite.org/download.html) must be in your PATH.

    ```
        pip install git+git://github.com/simonsfoundaion/anno-dbnsfp.git
    ```
    
    For help
    ```
        anno-dbnsfp -h
    ```
    
    Create an input file with mutations to be annotated.
    ```
        echo 'CHROM,POS,ID,REF,ALT,GENE
        13,23909440,.,G,A,SACS
        21,35144452,.,G,A,ITSN1
        1,180235688,.,G,A,LHX4
        7,73731910,.,C,T,CLIP2
        16,3820881,.,G,A,CREBBP
        3,113508666,.,A,G,ATP6V1A
        7,148512615,.,T,C,EZH2
        11,8111646,.,A,C,TUB
        3,21606142,.,G,T,ZNF385D
        9,37015066,.,T,A,PAX5
        2,223917672,.,G,A,KCNE4
        16,71318883,.,T,C,CMTR2
        18,21331038,.,A,G,LAMA3
        17,78831603,.,G,A,RPTOR
        12,49334805,.,A,G,RP11-302B13.5
        5,145603023,.,C,T,RBM27
        10,104596833,rs104894138,G,A,CYP17A1
        12,120436359,.,G,A,CCDC64
        1,213145953,.,C,T,VASH2' > test-mutations.csv
        
    ```

    Annotate

    ```
        anno-dbnsfp.py --genome_build=hg19 --input_delim=csv test_mutations.csv
        cat test_mutations.csv.ann.tsv
    ```

    To see all available dbNSFP columns
    ```
        anno-dbnsfp.py -p test_mutations.csv 
    ```



