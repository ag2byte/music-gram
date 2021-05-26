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
  console.log(JSON.stringify(selecteddict));

  fetch("/testfunction", {
    method: "POST",
    body: JSON.stringify({ value: selecteddict }),

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

  // var xhr = new XMLHttpRequest();
  // xhr.open("POST", "/testfunction", true);
  // // xhr.setRequestHeader("Content-Type", "application/json");
  // xhr.send("GEllo");
}
