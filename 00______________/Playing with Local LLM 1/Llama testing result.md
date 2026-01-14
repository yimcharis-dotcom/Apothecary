
Test subject: Llama model Llava Llama3
Testing: Extract information from an PDF. Url on the Pdf are not true URL 
>(URLs are annotations; model only sees copied text) [^1]

Process time: 20 mins

# [[Llama testing result]]
    
## What worked
LLM can format code+title+date when given clean copied text.​
Complied with instruction to output CSV format table 
    
## What failed
URLs were hallucinated because URLs aren’t in the text layer; need hyperlink extraction.

Output is as follow:
> 
> Here's the output in a CSV format:
> 
> |Standard Code|Standard Name|URL|Resolved Issue Date|
> |---|---|---|---|
> |P.1|MEMBERS' HANDBOOK CONTENTS OF VOLUME II (Updated to October 2025)|[https://www.hkfrs.org.hk/contents-vol-ii](https://www.hkfrs.org.hk/contents-vol-ii)|10/25|
> |HKAS 1|Presentation of Financial Statements|[https://www.hkiasc.org.hk/en/content/presentation-financial-statements](https://www.hkiasc.org.hk/en/content/presentation-financial-statements)|12/07|
> |HKAS 2|Inventories|[https://www.hkiasc.org.hk/en/content/inventories](https://www.hkiasc.org.hk/en/content/inventories)|3/04|
> |HKAS 7|Statement of Cash Flows|[https://www.hkiasc.org.hk/en/content/statement-cash-flows](https://www.hkiasc.org.hk/en/content/statement-cash-flows)|12/04|
> |HKFRS 1|First-ime Adoption of Hong Kong Financial Reporting Standards|[https://www.hkfrs.org.hk/first-time-adoption](https://www.hkfrs.org.hk/first-time-adoption)|12/08|
> |HKFRS 7|Financial Instruments: Disclosures|[https://www.hkfrs.org.hk/en/content/disclosure-financial-instruments](https://www.hkfrs.org.hk/en/content/disclosure-financial-instruments)|9/05|
> |HKFRS 10|Consolidated Financial Statements|[https://www.hkfrs.org.hk/en/content/consolidated-financial-statements](https://www.hkfrs.org.hk/en/content/consolidated-financial-statements)|12/08|
> |HKFRS 19|Presentation and Disclosure in Financial Statements|[https://www.hkfrs.org.hk/en/content/presentation-and-disclosure-financial-statements](https://www.hkfrs.org.hk/en/content/presentation-and-disclosure-financial-statements)|7/24|
> 
> Note: The URLs are not actual links as the PDF was not accessible.

## For doing better next time

1. Better prompting: 

> You are doing strict information extraction. Extract ONLY what is explicitly present in the provided text. Do NOT guess or create URLs.  
> If a field is missing, output `NULL`.  
> For each row, also provide `evidence` = the exact text snippet used.  
> Output a Markdown table with columns: standard_code, standard_name, url, issue_date, evidence.

2.   Consider the advice from pplx ai **reduceing hallucinations** #ai/strategy

> These two rules (NULL + evidence) are widely used to reduce hallucinations in extraction workflows.​
> A simple manual check (30 seconds)
> 
> Before trusting the output:
> Pick 2 rows and confirm each “URL” string literally appears in the input text. If not, it’s a hallucination and the prompt needs the NULL/evidence rules #prompt 

[^1]: Pplx comment
