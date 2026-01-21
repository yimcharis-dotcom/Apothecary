
# This looks more reasonable now
<img src="https://emoticons.hzchu.top/emoticons/Blob/blobcatthink.png" alt="Blob_blobcatthink" title="Blob_blobcatthink" class="emoji-image"> 
Others are good enough
Please put them all together in 1reply with their respective texts. Do include commentary not related to the uses and limits

Here is the complete **Perplexity Pro Plan** reference set for **December 16, 2025**, structured exactly like your backbone tables.

***[[# Master Note – Perplexity Pro (Dec 2025)

## 1. Text \& Model Usage (Pro)

| Event ID | Resource | Unit Charged | Typical Pro Allowance | Window | Limit Action |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **PPLX-P1** | **Pro Search (Flagship)**<br>*(GPT-5.2, Gemini 3 Pro, Claude 4.5 Sonnet)* | 1 search query | **300+ searches** | 24 hrs (rolling) | Fallback to Quick/Sonar |
| **PPLX-P2** | **Reasoning Models**<br>*(Sonar Reasoning, GPT-5.2 Thinking)* | 1 reasoning query | **~500 searches** | 24 hrs (rolling) | Switch to Standard |
| **PPLX-P3** | **Quick Search**<br>*(Sonar, GPT-4o-mini, Gemini 2.5 Flash)* | 1 prompt | **Unlimited** | None | None |
| **PPLX-P4** | **Deep Research** | 1 report | **High Cap** (Not unlimited) | Daily | Queue / Temp disable |

**Status Check (Dec 2025):**

* **Pro vs. Max:** The "Pro" plan (\$20/mo) includes standard flagship models. Ultra-high-compute models (like **o3-Pro** and **Claude 4.5 Opus**) are now exclusive to the **Max** plan (\$200/mo).
* **DeepSeek R1:** While the standalone "R1-1776" menu item was removed in August 2025, its capabilities are integrated into **Sonar Reasoning**, with a generous daily limit of ~500 queries.
* **Daily Reset:** The search limit is a **rolling 24-hour window**, meaning quota recovers gradually based on when you used it yesterday, not at midnight.

***

## 2. File System / Uploads (Pro)

| Event ID | Resource | Unit Charged | Typical Pro Allowance | Window | Limit Action |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **FILE-P1** | **File Upload (Chat)** | 1 batch | **~10–20 files** | Immediate | Upload blocked |
| **FILE-P2** | **File Size** | MB | **50 MB** per file | Per file | Upload fails |
| **FILE-P3** | **Space Storage** | Files per Space | **50 files** (Hard Cap) | Per Space | "Limit Reached" error |
| **FILE-P4** | **Context Window** | Tokens | **~2M** (Gemini 3) / **~200k** (Others) | Per query | Older files dropped |

**Note:** The **50-file limit per Space** remains the strictest constraint for power users. Unlike chat context which "slides," this is a hard storage cap that requires manual deletion to free up space.

***

## 3. Pages \& Spaces (Pro)

| Event ID | Resource | Unit Charged | Typical Pro Allowance | Window | Limit Action |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **PAGE-P1** | **Page Creation** | 1 page | **Unlimited** | N/A | None |
| **PAGE-P2** | **Space Creation** | 1 space | **Unlimited** | N/A | None |
| **PAGE-P3** | **Labs / Projects** | 1 project | **Limited** | Daily | Upgrade to Max |

**Status Check:** While creating Pages is unlimited, advanced interactive features in **Perplexity Labs** are now quota-limited for Pro users, with unlimited access reserved for the Max tier.

***

## 4. Image / Vision (Pro)

| Event ID | Resource | Unit Charged | Typical Pro Allowance | Window | Limit Action |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **IMG-P1** | **Image Generation**<br>*(Flux Pro, DALL-E 3)* | 1 image | **~50 images** | 24 hrs (rolling) | Tool disabled |
| **IMG-P2** | **Video Generation**<br>*(Veo 3.1)* | 1 video | **Limited** (Short clips) | Daily | Upgrade to Max |
| **IMG-P3** | **Image Analysis** | 1 analysis | Shared with Pro Search | 24 hrs | Fallback to Quick |

**Note:** The image limit is strict (~50/day) and separate from your text search quota. Hitting this limit does not stop you from asking text questions.

***

## 5. Data Analysis / API (Pro)

| Event ID | Resource | Unit Charged | Typical Pro Allowance | Window | Limit Action |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **API-P1** | **API Credits** | USD | **\$5.00 / month** | Monthly (1st) | Card charged for excess |
| **DA-P1** | **Code Execution** | 1 run | Shared with Search | Rolling | Standard throttle |

**Status Check:** The **\$5 monthly API credit** is a persistent perk. It does not roll over; use it or lose it each month.

***

## 6. Web / Browse (Pro)

| Event ID | Resource | Unit Charged | Typical Pro Allowance | Window | Limit Action |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **WEB-P1** | **Pro Search (Deep)** | 1 search | **300+ searches** | 24 hrs (rolling) | Fallback to Quick |
| **WEB-P2** | **Quick Search** | 1 search | **Unlimited** | N/A | None |
| **WEB-P3** | **Comet Browser** | 1 action | **Included** | N/A | None |


***

## Quota Enforcement Order (Dec 2025)

1. **Reasoning Fallback:** *(Sonar Reasoning Pro → Standard Sonar / GPT-5)*
*Explanation: If the "Thinking" model is overloaded or hits the daily cap, Perplexity silently switches to a standard fast model.*[^15]
2. **Search Fallback:** *(Pro Search → Quick Search)*
*Explanation: After ~300+ deep searches, the system stops doing multi-step web browsing and switches to single-shot fast answers.*[^16]
3. **Hard Stop:** *(Image Gen \& Space Files)*
*Explanation: Unlike text which degrades gracefully, image generation and Space uploads simply block you when the limit is reached.*[^2]

***

## Practical Quota Summary (Pro)

| Event / Tool | What counts as 1 use | Practical Pro limit (typical) | Reset behavior | What happens at limit |
| :-- | :-- | :-- | :-- | :-- |
| **Pro Search (Flagship)** | One complex query | **~300–600 per day** | Rolling 24h | Fallback to Quick Search |
| **Reasoning (Thinking)** | One "thought" query | **~500 per day** | Rolling 24h | Switch to Standard |
| **Quick Search** | One standard query | **Unlimited** | N/A | None |
| **Image Generation** | One image | **~50 per day** | Rolling 24h | Feature disabled |
| **Deep Research** | One report | **High Cap** (Not unlimited) | Daily | Queue / Temp disable |
| **Space Storage** | One file in Space | **50 files per Space** | **Manual delete** | "Limit Reached" error |
| **Chat File Uploads** | One file | **~20 per chat** | Per session | Upload blocked |
| **API Credits** | API Usage | **\$5.00 included** | Monthly (1st) | Card charged |]]
<div align="center">⁂</div>


