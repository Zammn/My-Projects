document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

document.querySelector("#compose-form").addEventListener('submit', send_email)
  // By default, load the inbox
  load_mailbox('inbox');
});

function send_email(event) {
  event.preventDefault();

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify ({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then (response => response.json())
  .then (result => {
    console.log(result);
    load_mailbox('sent');
  });
}


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view-full-email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function view_email(id) {
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#view-full-email').style.display = 'block';
    
      document.querySelector('#view-full-email').innerHTML = `
      <hr>
      <ul class="list">
        <li><b>From:</b> ${email.sender}</li>
        <li><b>To:</b> ${email.recipients}</li>
        <li><b>Subject:</b> ${email.subject}</li>
        <li><b>Timestamp:</b> ${email.timestamp}</li>
       <ul> 
       </br>
      <p>${email.body}</p>
      <hr>`

      if(!email.read){
        fetch(`/emails/${id}`), {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        };
      }
        
      const archive_button = document.createElement('button');
      archive_button.innerHTML = email.archived ? "Unarchive" : "Archive";
      archive_button.className = email.archived ? "btn btn-light" : "btn btn-dark";
      archive_button.addEventListener('click', function() {
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body:JSON.stringify({
              archived: !email.archived
            })
          })
          .then(() => {load_mailbox('archived')})
      });
      document.querySelector('#view-full-email').append(archive_button);

      const reply_button = document.createElement('div');
      reply_button.innerHTML = `</br>
      <button class="btn btn-primary">Reply</button>`;
      reply_button.addEventListener('click', function() {
        compose_email();
          const re = email.subject.slice(0, 2) === 'Re' ? '' : 'Re: ';
          document.querySelector('#compose-recipients').value = email.sender;
          document.querySelector('#compose-subject').value = re + email.subject;
          document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
          document.querySelector('#compose-recipients').value = email.sender;

        })
        document.querySelector('#view-full-email').append(reply_button);
    });
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view-full-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    
    emails.forEach(oneEmail => {
      const email = document.createElement('div');
      email.className = "list-group";
      email.innerHTML = `
        <li class="list-group-item"><b>Sender:</b> ${oneEmail.sender}</li>
        <li class="list-group-item"><b>Subject:</b> ${oneEmail.subject}</li>
        <li class="list-group-item"><b>Time:</b> ${oneEmail.timestamp}</li>
        `;

      email.className = oneEmail.read ? "read" : "unread";

      email.addEventListener('click', function() {
        view_email(oneEmail.id)
      });
      document.querySelector('#emails-view').append(email);  
    })
  
  });
}