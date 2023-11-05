const APIEndpoint = "http://127.0.0.1:5000"

inputEl = document.getElementById("articleLinkInput");
inputEl.focus();
inputEl.select();
inputEl.addEventListener("keydown", function (e) {
    if (e.code === "Enter") {  //checks whether the pressed key is "Enter"
        getArticle();
    }
});

async function getArticle() {
    articleURL = encodeURIComponent(document.getElementById("articleLinkInput").value);
    const response = await fetch(APIEndpoint + "/getResults/", {
        headers: {"articleURL": articleURL}
    }).then(res => res.text()).then(json => fillContent(json));
}

async function jsonTest() {
    const response = await fetch("./testData.json").then(res => res.text()).then(json => fillContent(json));
}

function fillContent(articles) {
    const articleObj = JSON.parse(articles);
    // console.log(articleObj);
    for (let i = 0; i < 4; i ++) {
        let column = document.getElementById("col"+String(i));
        articleList = articleObj[String(i)];
        // console.log(articleList)
        for (let j = 0; j < articleList.length; j ++) {
            // console.log(articleList[j]);
            let articleEl = document.createElement("a");
            articleEl.classList.add("article");
            let title = document.createElement("h3");
            title.innerHTML = decodeURIComponent(articleList[j]['title']);
            let source = document.createElement("p");
            source.innerHTML = decodeURIComponent(articleList[j]['source']);
            articleEl.setAttribute('href', articleList[j]['url']);
            articleEl.appendChild(title);
            articleEl.appendChild(source);
            column.appendChild(articleEl);
        }
    }
}