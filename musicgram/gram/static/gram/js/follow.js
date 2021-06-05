function follow() {
  console.log("Clicked");

  var profilecard = document.getElementById("profilecard");
  let to_be_followed = profilecard.getAttribute("data-name");
  let followed_by = profilecard.getAttribute("data-myname");
  console.log(to_be_followed, followed_by);

  // create a fetch request here

  fetch("/follow", {
    method: "POST",
    body: JSON.stringify({
      to_be_followed: to_be_followed,
      followed_by: followed_by,
    }),

    headers: {
      "Content-type": "application/json;",
    },
  }).then((res) => {
    if (res.status == 201)
      // all good
      console.log("Alll good");

    document.getElementById("followbutton").style.display = "none";
    followers = document.getElementById("followers");
    let count = parseInt(document.getElementById("followers").innerText) + 1;
    followers.innerText = count;
  });
}
