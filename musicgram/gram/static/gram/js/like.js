function likeunlike(songid, isliked) {
  // you have to like id with the currrent user
  console.log("Songid: " + songid);
  console.log("isLiked: " + isliked);
  //   console.log("USerID: " + userid);

  if (isliked == "false") {
    fetch("/like", {
      method: "POST",
      body: JSON.stringify({ songid: songid }),

      headers: {
        "Content-type": "application/json;",
      },
    }).then((res) => {
      if (res.status == 201) {
        // all good
        console.log("all good");
        document.getElementById("img-" + songid).src =
          "https://img.icons8.com/cotton/64/000000/like--v3.png";

        document
          .getElementById("img-" + songid)
          .setAttribute("data-isliked", "true");
        let count =
          parseInt(document.getElementById("likes-" + songid).innerText) + 1;
        document.getElementById("likes-" + songid).innerText = count;
      }
      window.location.reload();
    });
  } else if (isliked == "true")
    fetch("/unlike", {
      method: "POST",
      body: JSON.stringify({ songid: songid }),

      headers: {
        "Content-type": "application/json;",
      },
    }).then((res) => {
      if (res.status == 201) {
        // all good
        console.log("all good");
        document.getElementById("img-" + songid).src =
          "https://img.icons8.com/ios/50/000000/hearts.png";

        document
          .getElementById("img-" + songid)
          .setAttribute("data-isliked", "false");
        let count =
          parseInt(document.getElementById("likes-" + songid).innerText) - 1;
        document.getElementById("likes-" + songid).innerText = count;
        window.location.reload();
      }
    });
}
function unlike(songid) {
  // you have to like id with the currrent user
  console.log("Songid: " + songid);
  //   console.log("USerID: " + userid);
}
