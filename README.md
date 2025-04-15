# arc-id-classifier

The Alien Resident Certificate (ARC) serves as a temporary ID card for foreign residents in Taiwan.
Since ARC numbers have a format similar to Taiwanese IDs, distinguishing between them can be challenging. This tool helps quickly identify whether the holder is a foreign resident or a Taiwanese citizen.

Old Format: Issued before January 1st, 2022 (two letters + eight digits, e.g., AB12345678).
New Format: Issued after January 2nd, 2022 (one letter + nine digits, e.g., A123456789).

Current Version:

- Differentiate between Taiwanese national IDs and Alien Resident Certificates (ARC) by analyzing the structure of the ARC/ID numbers (both old and new format).
- Classifies the holder’s status (foreign national, Mainland Chinese, Hong Kong/Macau resident).
- Provides a downloadable version of the results.

Deployed on Streamlit: https://arc-id-classifier.streamlit.app/
.
