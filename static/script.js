function like(postId) {
    const likeCount = document.getElementById(`like-counter-${postId}`) 
    const likeButton = document.getElementById(`like-post-${postId}`) 

    fetch(`/like-post/${postId}`,{method:"POST"}).then((res) =>
        res.json()
    )
    .then((data) => {
        likeCount.innerHTML=data["likes"]+" Likes";
        if (data["liked"] === true){
            likeButton.className = "fas fa-heart"
        }
        else{
            likeButton.className = "far fa-heart"
        }
    })

    console.log(likeCount.value)

}

// function loader() {
    

// }