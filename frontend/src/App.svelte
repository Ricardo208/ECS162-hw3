<script lang="ts">
  import { onMount } from "svelte";


  let apiKey: string = "";
  let articles: any[] = [];

  onMount(async () => {
  try {
    const res = await fetch('/api/nyt'); // Fetch from your backend
    const data = await res.json();
    const docs = data?.response?.docs;
    if (Array.isArray(docs)) {
      articles = docs;
    }
  } catch (error) {
    console.error("Failed to fetch NYT articles:", error);
  }
});

</script>


<header>  <!-- put all the drop down stuff here nav bar, logo and text here -->
  <div class = header-row>
      <div class = header-left-text>
          <p> <strong> Monday, April 14, 2025 </strong> </p>
          <p>Today's Paper</p>
      </div>

      <div class = header-center-logo>
          <img src="/images/logo.png" alt="Logo" id="logo"> 
      </div>

      <div class = header-right-empty> <!-- in order to center the logo within the flex container, I added an empty spacer-->
      </div>
  </div>
</header>
<hr> <!-- Mimics the horizontal line that borders the header and content -->
<hr>


<main>
  <div class="container">  <!-- Created a contanier to hold each content within its own column and to use flex -->
    {#each articles.slice(0, 3) as article, i} <!-- https://svelte.dev/docs/svelte/each -->
    <section class="column column-{String.fromCharCode(97 + i)}" data-id={article._id}> <!-- class names generated using AI, documented in README -->

        <!-- references to article properties given from example here: https://github.com/nytimes/public_api_specs/blob/master/article_search/article_search_v2.md -->
        <h2>{article.headline.main}</h2>
        <p>{article.snippet}</p>

        <!-- based on the json: https://api.nytimes.com/svc/search/v2/articlesearch.json?q=Davis%20OR%20Sacramento&api-key=SB6lFTn1ORTocZc7OkMnLZi5WA24YSDd-->
        {#if article.multimedia && article.multimedia.default && article.multimedia.default.url}
          <img
            src={article.multimedia.default.url} 
            alt={article.headline.main}x
            style="max-width: 100%; height: auto;"
          />
        {/if}

        <a href={article.web_url} target="_blank" rel="noopener noreferrer">Read More</a>

      </section>
    {/each}
  </div>
</main>
<style>

  body {
    background: white;
  }
  .header-row{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
    margin-bottom: 5px;
    margin-left: 30px;
    margin-right: 30px;
}

.header-left-text{
    display: flex;
    flex-direction: column;
    font-size: 14px;
    font-family: 'Helvetica Neue', Arial, Helvetica, sans-serif;
}

.header-center-logo{
    flex: 0;
    display: flex;
    justify-content: center;

}

.header-right-empty{
    display: flex;
    width: 150px;
}

.header-left-text p{
    margin: 0;
}

.container{
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    margin: 0;
}

.column{
    flex: 1;
    padding: 20px;
    margin: 3px;
    font-size: 12pt;
    min-height: 300px;
    font-family: Georgia;
    border-bottom: 1px solid #ccc;
}

.column-a{
    border-right: 1px solid #ccc;
    
}

.column-b{
    border-right: 1px solid #ccc;
}

hr {
    width: 90%;
    margin: auto;
}

#logo {
    width: 500px;
    height: auto;
  }

#pikachu {
    width: 200px;
    height: auto;
    display: block;
    margin: 0 auto;
  }

#breloom{
    width: 250px;
    height: auto;
    display: block;
    margin: 0 auto;
}

#aipom{
    width: 300px;
    height: auto;
    display: block;
    margin: 0 auto;
}

/* Decreases size in header row items, updates columns to only display two, removes right border from second column */
@media only screen and (min-width: 768px) and (max-width: 1024px){
    .header-left-text{
        font-size: 10pt;
    }

    .header-right-empty{
        display: flex;
        width: 100px;
    }
    .container{
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
    }
    .column{
        flex: 0 0 50%;
        width: 50%;
        box-sizing: border-box;
        margin: 0;
        padding: 10px;
    }

    .column-b{
        border-right: none;
    }

    .column-c{
       flex: 0 0 100%;
       max-width: 100%;
    }

    #logo{
        width: 300px;
        height: auto;
    }
}

/* Decreases size in header row items, updates columns to only display one, removes right border from firt and second column */
@media only screen and (max-width: 767px){
    .header-left-text{
        font-size: 8pt;
    }

    .header-right-empty{
        display: flex;
        width: 60px;
    }
    .container{
        flex-direction: column;
    }
    .column{
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        border-right: none;
    }
    
    #logo{
        width: 270px;
        height: auto;
    }

    hr {
        max-width: 100%;
    }
}
</style>
