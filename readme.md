# IRR Communities Parser


A RegEx-based parser to collect BGP Communities information from IRR's aut-num objects.


##  Introduction

Communities are optional BGP attributes used to communicate routing intentions between Autonomous Systems (ASes) and to carry out some traffic engineering actions on the Internet. Each AS defines its own Communities' values ​​and semantics, but there is no formal means for publishing this information.

In general, the set of communities used by an AS can be found on the AS' website or in its routing policies record made available by the Internet Routing Register (IRR).  Routing policy records can be obtained through WHOIS queries intermediated by some WHOIS Web service or executed directly from the command line, as shown below.

	  whois -h whois.some_irr_server.net AS<Autonomous_System_Number>

When compared to searching in ASes Websites (there are tens of thousands of ASes), IRR is more suitable for collecting information in batches (all IRR servers supposedly provide the same set of records). This centralization of information greatly simplifies the collection and parsing processes.

The IRR has several types of records (called objects), each responsible for storing a certain type of information about ASes. Aut-num objects describe ASes' routing policies and are the main source of information on community semantics in IRR. Not all aut-num objects contain Communities' information and, among those that do, not all present it in an intelligible descriptive form (there is no standard format). 

The aim of this project is to facilitate the task of identifying, collecting and classifying BGP Communities through the automated analysis of IRR responses.

## Scope
The current implementation of the **IRR Communities Parser** is capable of recognizing the following 32-bit community types: 

 - Prepend (with Prepend number)
 - Blackhole
 - No-Export
 - No-Advertise

## Usage

### Prerequisites

 - [python 3.6+](https://www.python.org/downloads/])
 - [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)

### Input

    IRR objects stored locally as .txt files named after its source ASN
  Example: 
	    The following query will return a AS47065 IRR object:
	    
					    whois -h whois.arin.net a AS47065
	     
The response from this query should be named *47065.txt* and stored in the parser's  input directory (at the root or in one of its subdirectories).

### Output
A *.json* and a *.csv* files containing the collected data.

**json:**

    {ASN: {
	    Community_type: {
		    Community_value : Community_description
						}
		 }
	{
    
**csv:**

    
|ASN|Community_type|Community_value|Community_description| 
|---|--------------|---------------|---------------------|


#### Defaults

Defaults can be edited in *./utils/defaults.py*
 - input dir: *./data/irr/*
 - output dir: *./data/communities/*
 - output filenames: *communities.json* and *communities.csv*

### Command-line arguments

    python parse.py [-h] [-i input_dir] [-o output_dir]

 - All arguments are optional.
 - In the absence of an argument, its default value will be used.



## Extensibility
**IRR Communities Parse** is designed to be easily extendable. To make it search for a new type of Community, 

 1. choose a lowercase term to call your new type (*type_reference_name*),
 2. extend the class *CommunityTypes* in *./_types/type_parser.py* with a new type class(you can use *blackhole.py* as a model),
 3. add the new type's specific RegEx pattern to the *./_types/commons/patterns.py* file  (assigned to a variable named after the chosen *type_reference_name* ),
 4.  instantiate the new class in *./parse.py*  (assigned to a *type_reference_name* class variable),  
 5. add the *type_reference_name* to the type list in *./parse.py*.



## Authors

* **Paulo Mol** - *Initial work* - [pmolufmg](https://github.com/pmolufmg)

See also the list of [contributors](https://github.com/pmolufmg/IRR_Communities_Parser/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## References

 - [Chandra, R., P. Traina, and T. Li. "RFC1997: BGP Communities Attribute." (1996).](https://dl.acm.org/doi/pdf/10.17487/RFC1997)
 - [Bayraktar, S. "Policy Behavior for Well-Known BGP Communities." _Policy_ (2019).](https://andrew-scott.co.uk/docs/rfc-pdf/rfc8642.txt.pdf)
 - [Alaettinoglu, Cengiz, et al. "Routing Policy Specification Language (RPSL)." _RFC_ 2622 (1999): 1-69.](https://tools.ietf.org/html/rfc2622)
 - [Daigle, Leslie. "WHOIS protocol specification." _RFC 3912 (Draft Standard)_ (2004).](https://tools.ietf.org/html/rfc3912)
 - [https://whois.icann.org/en/basics-whois](https://whois.icann.org/en/basics-whois)
 - [https://www.iana.org/assignments/as-numbers/as-numbers.xhtml](https://www.iana.org/assignments/as-numbers/as-numbers.xhtml)
 - [http://www.irr.net/](http://www.irr.net/)
