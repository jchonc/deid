# A NLP based PHI de-identification method

## Vocabulary & Abbreviations

* NLP - [Nature Language Processing](https://en.wikipedia.org/wiki/Natural_language_processing)
* PHI - [Protected Health Information](https://en.wikipedia.org/wiki/Protected_health_information)
* [De-Identification](https://en.wikipedia.org/wiki/De-identification) 

## Core challenge for Lucas

Often we have to test/experiment/research on the free text data from our clients, but we have to erase all the information which could bge used to trace back to the individual.  For example, the following text:

> Mr. James Bond has visited us at 12/12/2018 at 3:00PM for this routine doctor's appointment. Dr. Ethan Hunt has noted his left hand has some rash.

Obviously both names need to be erased to prevent revealing too much information. But there more, all identification data need to be removed. According to [HIPAA](https://en.wikipedia.org/wiki/Health_Insurance_Portability_and_Accountability_Act), we have to remove:

 Names
* Geographic subdivisions smaller than a state
* All elements of dates (except year) related to an individual (including admission and discharge dates, birthdate, date of death, all ages over 89 years old, and elements of dates (including year) that are indicative of age)
* Telephone, cellphone, and fax numbers
* Email addresses
* IP addresses
* Social Security numbers
* Medical record numbers
* Health plan beneficiary numbers
* Device identifiers and serial numbers
* Certificate/license numbers
* Account numbers
* Vehicle identifiers and serial numbers including license plates
* Website URLs
* Full face photos and comparable images
* Biometric identifiers (including finger and voice prints)
* Any unique identifying numbers, characteristics or codes

## What we knew already

From the [earlier project](nlp-react) we have a limited way to parse/tag various part of the sentences. 

## What we want you to deliver

## Pre-requisite

* GitHub
* Python
* [TDD](https://en.wikipedia.org/wiki/Test-driven_development)
* [SpaCy](https://spacy.io/)
* [Regular Expression](https://en.wikipedia.org/wiki/Regular_expression)

## Get Going

from within code, run "pip install -r requirements.txt"




