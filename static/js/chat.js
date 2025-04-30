let socket = new WebSocket("ws://" + window.location.host + "/ws/chat/");

socket.onmessage = function(event) {
    let data = JSON.parse(event.data);
    if (data.action === "delete") {
        document.querySelectorAll(".message").forEach(msg => {
            if (msg.dataset.sender === data.username) {
                msg.innerHTML = "<i>This message was deleted</i>";
            }
        });
    }
};

function deleteChat() {
    if (selectedUser === "") {
        alert("No chat selected.");
        return;
    }
    if (!confirm("Are you sure you want to delete this conversation?")) {
        return;
    }

    fetch(`/delete_chat/${selectedUser}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        if(data.success){
            document.querySelectorAll(".message").forEach(msg => {
                msg.innerHTML = "<i>This message was deleted</i>";
            });
            alert(data.success);
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error("Error deleting chat:", error);
        alert("An error occurred while deleting the chat.");
    });
}
