/* static/script.js */

// You can add any global JavaScript or HTMX-related scripts here
// Example: Handle dynamic content, animations, etc.

document.addEventListener("DOMContentLoaded", function () {
    console.log("Page loaded, all assets are ready!");

    // Add any other global JavaScript code here
});

function confirmDelete(playlistId) {
    const confirmed = confirm("Are you sure you want to delete this playlist?");
    if (!confirmed) return;
  
    fetch(`/deletePlaylist?playlistId=${playlistId}`, {
      method: 'DELETE',
    })
      .then((res) => {
        if (res.ok) {
          document.getElementById(`playlist-${playlistId}`).remove();
          alert("Playlist deleted.");
        } else {
          res.json().then(data => alert(data.error || "Failed to delete playlist."));
        }
      })
      .catch((err) => {
        console.error("Error:", err);
        alert("An error occurred.");
      });
  }