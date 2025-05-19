# ECS162 HW 1 README & Documentation of AI Usaage / References

## Code References 
* refrences are linked next to code that uses it.



## Generative AI Use
- Prompt: so if i want to give three divs the same foundational base, but i also want to make customizable changes to each div without affecting the others, how can i do that? for example, i want to have a base column settings in CSS, but be able to make changes to each column that doesnt affect the others

    - Response: div class="column column-a">...</div
                div class="column column-b">...</div
                div class="column column-c">...</div

- Prompt: how can i fetch and display saved comments from MongoDB when the comment section is toggled open?
    - Response: Use a GET request inside an async function like toggleComments, and fetch comments from /api/comments?articleId=....

- Prompt: in order for comments to be deleted only by moderators and not users, hwo can i use the email? or should i use their ids?
    - Response: In Flask, check if the logged-in user's email is "moderator@hw3.com" using session.get("user", {}).get("email").

- Prompt: why do my comments disappear after a page refresh even though i posted them?
    - Response: You may not be fetching them on page load or when the comment section is opened. Make sure to call your backend GET route after toggling comments.

- Prompt: why does MongoDB show "No default database defined" or "command insert requires authentication" in my tests?
    - Response: client = MongoClient("mongodb://root:rootpassword@localhost:27017/mydatabase?authSource=admin")





