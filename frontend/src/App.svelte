<script lang="ts">
  import { onMount } from "svelte";


  let apiKey: string = "";
  let articles: any[] = [];

  let showingCommentsPanel = false;
  let articleId = "";
  let showingComments = {};
  let commentInputs = {};
  let commentsByArticle = {};

  let user = null;

  onMount(async () => {
  try {
    const userRes = await fetch('/api/user');
    if (userRes.ok) {
      const userData = await userRes.json();
      if (Object.keys(userData).length > 0) {
        user = userData;
      }
    }


    const articleRes = await fetch('/api/nyt'); // Fetch from backend
    const articleData = await articleRes.json();
    articles = articleData.response?.docs || [];

  } catch (error) {
    console.error("Failed to fetch NYT articles:", error);
  }
});

  async function toggleComments(articleId){
    showingComments[articleId] = !showingComments[articleId];

    if (showingComments[articleId]) {
      try {
        const res = await fetch(`/api/comments?articleId=${encodeURIComponent(articleId)}`);
        //references: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API & https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/encodeURIComponent

        if (res.ok) {
          const data = await res.json();  
          //references: https://developer.mozilla.org/en-US/docs/Web/API/Response/json
          commentsByArticle[articleId] = data;
        } else {
          console.error("Failed to fetch comments");
        }
      } catch (error) {
        console.error("Error fetching comments:", error);
    }
  }
}

  async function submitComment(articleId){
    const text = commentInputs[articleId];
    if (text === undefined || text === null) return;


    const res = await fetch("/api/comments", { // saves the comment to our backend!
        method: "POST", // sends data to create a new comment 
        headers: { "Content-Type": "application/json" }, // sending in json format
        body: JSON.stringify({ articleId, text }), // stringify the text
      });

    if (res.ok) {  // if post succeeds 
      const newComment = await res.json();
      commentsByArticle[articleId] = [...(commentsByArticle[articleId] || []), newComment]; //update so that we can see comments on pate
      commentInputs[articleId] = ""; // clears comment tesxt area after we suhmit the comment
    } else {
      alert("Failed to post comment."); // error checking
    }
  }

  async function deleteComment(commentId, articleId) {
  try {
    const res = await fetch(`/api/comments/${commentId}`, {
      method: "DELETE" // references: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
    });

    if (res.ok) {
      // after we delete, refetch updated comment
      const updatedRes = await fetch(`/api/comments?articleId=${encodeURIComponent(articleId)}`);
      if (updatedRes.ok) {
        const data = await updatedRes.json();
        commentsByArticle[articleId] = data;
      }
    } else {
      console.error("Failed to delete comment");
    }
  } catch (error) {
    console.error("Error deleting comment:", error);
  }
}


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

      <div class = header-right-empty>
        <div class="header-right-account">
          {#if user}
            <p>Hello, {user.email} | <a href="http://localhost:8000/logout">Logout</a></p>
          {:else}
            <p><a href="http://localhost:8000/login">Log in</a></p>
          {/if}
        </div>
         <!-- in order to center the logo within the flex container, I added an empty spacer-->
      </div>
  </div>
</header>

<hr> <!-- Mimics the horizontal line that borders the header and content -->
<hr>

<main>
  <div class="container">  <!-- Created a contanier to hold each content within its own column and to use flex -->
    {#each articles.slice(0, 3) as article, i} <!-- https://svelte.dev/docs/svelte/each -->
    <section class="column column-{String.fromCharCode(97 + i)}" data-id={article._id}> <!-- class names generated using AI, documented in README -->

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

        <button on:click={() => {
          showingCommentsPanel = true;
          articleId = article._id;
          toggleComments(article._id);
        }}>
          Show Comments
        </button>
        <!-- references to article properties given from example here: https://github.com/nytimes/public_api_specs/blob/master/article_search/article_search_v2.md -->

      </section>
    {/each}
  </div>
</main>

{#if showingCommentsPanel}
  <div class="comment-modal">
    <div class="comment-header">
      <h3>Comments {commentsByArticle[articleId]?.length || 0}</h3>
      <button on:click={() => showingCommentsPanel = false}>✕</button>
    </div>

    <textarea bind:value={commentInputs[articleId]} placeholder="Share your thoughts..."></textarea>
    <button on:click={() => submitComment(articleId)}>Post</button>

    <ul>
      {#each commentsByArticle[articleId] || [] as comment}
        <li class="comment">
          <div class="avatar-placeholder">{comment.user?.charAt(0)}</div>
          <div class="comment-content">
            <strong>{comment.user}</strong>
            <p>{comment.text}</p>
            {#if user?.email === "moderator@hw3.com"}
              <button on:click={() => deleteComment(comment._id, articleId)}>Delete</button>
            {/if}
          </div>
        </li>
      {/each}
    </ul>
  </div>
{/if}

<style>
:root {
  --bg: #ffffff;
  --fg: #000000;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #121212;
    --fg: #ffffff;
  }

  .avatar-placeholder {
    background-color: #444;
  }
}

  body {
    background-color: var(--bg);
    color: var(--fg);
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
  align-items: center;
  justify-content: flex-end;
  font-size: 14px;
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


.comment-modal {
  background-color: var(--bg);
  color: var(--fg);
  position: fixed;
  right: 0;
  top: 0;
  width: 350px;
  height: 100%;
  border-left: 1px solid #ccc;
  padding: 1rem;
  overflow-y: auto;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
  z-index: 999;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.comment-header h3 {
  margin: 0;
  font-size: 1.25rem;
}

.comment-header button {
  border: none;
  background: none;
  font-size: 1.2rem;
  cursor: pointer;
}

.comment-modal textarea {
  width: 100%;
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ccc;
  margin-bottom: 0.5rem;
}

.comment-modal button[type="submit"] {
  display: block;
  margin-left: auto;
  margin-bottom: 1rem;
  padding: 0.4rem 0.8rem;
  padding-bottom: 10%;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.comment-modal button.delete-button {
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 1rem;
}

.comment-modal ul {
  list-style: none;
  padding-left: 0;
  margin: 0;
}

.comment {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  margin-bottom: 1rem;
}

.avatar-placeholder {
  width: 32px;
  height: 32px;
  background-color: #eee;
  border-radius: 50%;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
}

.comment-content {
  flex-grow: 1;
  text-align: left;
}

.comment-content p {
  margin: 0.2rem 0;
  text-align: left;
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
