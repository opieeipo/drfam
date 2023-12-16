# DrFAM
OpenAI Implementation for interrogating the [Foreign Affairs Manual(FAM)](https://fam.state.gov/) and [Department of State Standardized Regulations (DSSR)](https://aoprals.state.gov/Content/Documents/DSSRMaster20230827%20-%20Final%20Form.docx). of the Department of State.  About 35000 pages of text in total scraped and trained into OpenAI for natural language interrogation

**Prerequisites** 

If you don't already have it, get curl:

https://curl.se/download/curl-8.5.0.zip

**Windows Subsystem for Linux(WSL)**

The development started in Replit, moved to Windows, did some system upgrades and then wanted to move into more with GPU support -- so shifted to linux to simplify life (stranger words have never been spoken)

For more information on how to get this installed (has been available for several version of Windows now in multiple distribution flavors):

https://learn.microsoft.com/en-us/windows/wsl/install

**Windows**

>To setup the python environment(s) use the following

*pywinsetup.cmd*


**Linux**

>To setup the python environment(s) use the following

*pywslsetup.sh*

**Files of Import**
wsl.Requirements.Txt includes the necessary files for within linux that include some of the GPU Nvidia libraries not currently available to windows at the time of this project's creation.
This significantly improves query times (reduces by ~50%) but requires an environment with Nvidia GPU's.  This is usually comes at a premium with cloud based services so default option would be to use the CPU only version.  
The code includes autodetection for determining if GPU's are present or not by checking on torch.

https://pip.pypa.io/en/stable/installation/

I'll provide a separate repository for that that explains more in depth how that was created and can be refreshed later as needed.  Current rebuild time for that in sequence is about 2 hours (not including web scrape time)

**Postgres**


>Postgres needed for the user authentication and query storage

*Windows Download*

https://www.postgresql.org/download/windows/

*Linux Download*

sudo apt-get install postgres

*GUI for accessing your DB*

https://www.pgadmin.org/download/

**Suggested Reading**

For connecting to the Proxy on Google
https://cloud.google.com/sql/docs/postgres/connect-auth-proxy

**Environmental Variables**

>Environmental variable that need to be set prior to running:

**STORAGE**=`"BlobEndpoint=https://famdat.blob.core.windows.net/;QueueEndpoint=https://famdat.queue.core.windows.net/;FileEndpoint=https://famdat.file.core.windows.net/;TableEndpoint=https://famdat.table.core.windows.net/;SharedAccessSignature=sv=2022-11-02&ss=bfqt&srt=sco&sp=rlf&se=2024-10-31T22:00:17Z&st=2023-12-13T14:00:17Z&spr=https&sig=qjoVuvkCN65l3ZSnUmHp9huG5lc6HGZ1i%2FnwIUZsP0U%3D"`

*This is a shared read-only key that gets you the fam.faiss*

This project  does not include the training used to create the vectorDB.  I used FAISS.  To read more about that check out: 

https://faiss.ai/index.html

**OPEN_API_KEY**=`"sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`

*Requires an API key from OpenAPI*

https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/#:~:text=To%20get%20an%20API%20Key,this%20button%20to%20get%20one.

**PORT**=`XXXX`

This is the port your local instance will run on.

**Getting things running**

Make sure you have entered the appropriat python environment

for linux:

`source ./.dev.wsl.env/bin/activate`

*(to exit just type `deactivate`)*

for windows:

`.\.dev.windows.env\Scripts\activate.bat`

(to exit: `.\.dev.windows.env\deactivate.bat`)

**Startup Already!!**

`gunicorn -b :$PORT chatbot:app --timeout=120`








