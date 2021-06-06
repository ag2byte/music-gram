function followunfollow() {
  console.log("Clicked");

  var profilecard = document.getElementById("profilecard");
  let to_be_followed = profilecard.getAttribute("data-name");
  let followed_by = profilecard.getAttribute("data-myname");
  console.log(to_be_followed, followed_by);

  // create a fetch request here
  if (
    document.getElementById("followbutton").getAttribute("data-isfollowed") ==
    "false"
  ) {
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

      document.getElementById("followbutton").innerText = "Unfollow";
      document
        .getElementById("followbutton")
        .setAttribute("data-isfollowed", "true");

      followers = document.getElementById("followers");
      let count = parseInt(document.getElementById("followers").innerText) + 1;
      followers.innerText = count;
    });
  } else if (
    document.getElementById("followbutton").getAttribute("data-isfollowed") ==
    "true"
  ) {
    fetch("/unfollow", {
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

      document.getElementById("followbutton").innerText = "Follow";
      followers = document.getElementById("followers");
      document
        .getElementById("followbutton")
        .setAttribute("data-isfollowed", "false");
      let count = parseInt(document.getElementById("followers").innerText) - 1;
      followers.innerText = count;
    });
  }
}
