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

  fetch("/testfunction", {
    method: "POST",
    body: JSON.stringify(selecteddict),

    headers: {
      "Content-type": "application/json;",
    },
  })
    .then((res) => {
      return res.text();
    })
    .then((text) => {
      console.log(text);
    });
}
