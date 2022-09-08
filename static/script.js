document.getElementById("submit").addEventListener("click", function (e) {
  e.preventDefault();
  let longLink = document.getElementById("long-link").value;
  let body = {
    url: longLink,
  };
  if (longLink) {
    fetch("/api", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    })
      .then((res) => res.json())
      .then((json) => {
        if (navigator.clipboard) document.getElementById("copy").style.display = "flex";
        document.getElementById("shawt-link").value = `https://shawt.link/${json.link_id}`;
      });
  }
});

document.getElementById("copy").addEventListener("click", function () {
  // let copyText = document.getElementById("shawt-link");
  // copyText.select();
  // copyText.setSelectionRange(0, 99999); // For mobile devices

  // if (navigator.clipboard) navigator.clipboard.writeText(copyText.value);

  var text = document.getElementById("shawt-link").value;

  navigator.clipboard
    .writeText(text)
    .then(() => {
      console.log("Text copied to clipboard");
    })
    .catch((err) => {
      alert("Error in copying text: " + err);
    });
});
