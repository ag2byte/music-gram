function clickSong(id) {
  id = "#" + id;
  console.log(id);

  // getting details
  var selecteddict = {};

  selecteddict["imagelink"] = document
    .querySelector(id)
    .getAttribute("data-imglink");

  selecteddict["songname"] = document
    .querySelector(id)
    .getAttribute("data-name");

  selecteddict["artist"] = document
    .querySelector(id)
    .getAttribute("data-artist");

  selecteddict["songlink"] = document
    .querySelector(id)
    .getAttribute("data-link");

  console.log(selecteddict);
  // console.log(JSON.stringify(selecteddict));

  fetch("/addpost", {
    method: "POST",
    body: JSON.stringify({ value: selecteddict }),

    headers: {
      "Content-type": "application/json;",
    },
  }).then((res) => {
    if (res.status == 201)
      // all good
      window.location.pathname = "/createpost";
  });

  // var xhr = new XMLHttpRequest();
  // xhr.open("POST", "/addpost", true);
  // xhr.setRequestHeader("Content-Type", "application/json");
  // xhr.send("GEllo");
}
