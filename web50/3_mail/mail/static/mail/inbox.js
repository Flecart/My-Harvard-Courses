document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  //
  document.querySelector("#compose-submit").addEventListener("click", () => send_mail());
});

function compose_email() {

  show('compose-view')

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function reply_email(old_mail) {
  show('compose-view')

  // prefill composition fields
  document.querySelector('#compose-recipients').value = old_mail.sender;
  document.querySelector('#compose-subject').value = `Re: ${old_mail.subject}`;
  document.querySelector('#compose-body').value = `On ${old_mail.timestamp} ${old_mail.sender} wrote: ${old_mail.body}`;
}

function load_mailbox(mailbox) {

  show('emails-view')

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  show_mailbox(mailbox)
}

function show_email(id) {

  show('single-email')
  fetch(`emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true,
    })
  })

  fetch(`emails/${id}`, {
    method: "GET",
  })
  .then(response => response.json())
  .then(result => {

    err = check_error(result)
    if (!err) {
      // handle archive unarchived
      let text, archived;
      if (result.archived) {
        text = "Unarchive Email";
        archived = false;
      } else {
        text = "Archive Email";
        archived = true;
      }

      const element = document.createElement('div');
      element.className = 'card my-4';
      element.innerHTML = `
        <div class="d-flex card-header justify-content-between">
          <div class=" h3 flex-item">
            ${ result.subject }
          </div>
          <div class=" flex-item"> ${ result.timestamp } </div>
        </div>
        <div class="card-body">
        <p> ${ result.body } </p>
          <blockquote class="blockquote mb-0">
            <footer class="blockquote-footer">Sent by <cite title="Source Title">${ result.sender }</cite></footer>
            <footer class="blockquote-footer">Sent to <cite title="Source Title">${ result.recipients }</cite></footer>
              <div class="d-flex justify-content-between">
                <button class="btn btn-primary mt-3" id="archive-${ result.id }"> ${ text } </button>
                <button class="btn btn-primary mt-3" id="reply"> Reply </button>
              </div>
            </blockquote>
        </div>
      `;
  
      document.querySelector('#single-email').append(element)
  
      document.querySelector(`#archive-${result.id}`).addEventListener('click', () => {
        fetch(`emails/${id}`, {
          method: "PUT",
          body: JSON.stringify({
          archived: archived,
          })
        })

        load_mailbox('inbox')
      })

      document.querySelector(`#reply`).addEventListener('click', () => {
        reply_email(result)
      })
    }
  })
}

function send_mail() {

  // Get needed info 
  recipients = document.querySelector('#compose-recipients').value;
  subject = document.querySelector('#compose-subject').value;
  body = document.querySelector('#compose-body').value;

  // send request with REST API
  fetch("emails", {
    method: "POST", 
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    })
  })
  .then(response => response.json())
  .then(result => {
    check_error(result)
  })
  
  load_mailbox("sent")
}

// UTILS

// Resets everything to show only the div with field_id
function show(field_id) {

  document.querySelector("#alert").hidden = true
  // history.pushState({mailbox: "compose"}, "", "compose")

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email').style.display = 'none';

  // empty email fiels
  document.querySelector('#emails-view').innerHTML = ""
  document.querySelector('#single-email').innerHTML = ""

  document.querySelector(`#${field_id}`).style.display = 'block';

}

function check_error(response) {
  alert_div = document.querySelector("#alert");
  if ("error" in response) {
    alert_div.className = 'alert-danger alert';
    alert_div.innerHTML = response['error'];
    alert_div.removeAttribute("hidden");
    return true;
  } else if ("message" in response) {
    alert_div.className = 'alert-success alert';
    alert_div.innerHTML = response['message'];
    alert_div.removeAttribute("hidden");
  }

  return false;
}

function show_mailbox(mailbox) {
  fetch(`emails/${mailbox}`, {
    method: "GET",
  })
  .then(response => response.json())
  .then(result => {
    result.forEach(email => {

      console.log(email);
      // provide feedback if email has been read
      let read_icon;
      if (email.read) {
        read_icon = `<i class="bi bi-square-fill" style="color:green"></i>`;
      } else {
        read_icon = `<i class="bi bi-square-fill" style="color:red"></i>`;
      }

      const element = document.createElement('div');
      element.className = 'card my-4';
      element.innerHTML = `
        <div class="card-header h3">
          ${ email.subject }
        </div>
        <div class="card-body">
          <blockquote class="blockquote mb-0">
            <p> ${ email.timestamp } </p>
            <footer class="blockquote-footer">Sent by <cite title="Source Title">${ email.sender }</cite></footer>
            <footer class="blockquote-footer">Sent to <cite title="Source Title">${ email.recipients }</cite></footer>
            <div class="d-flex justify-content-between align-items-center">
              <button class="btn btn-primary mt-3 " id="email-${ email.id }"> See email </button>
              <div class="">${read_icon}</div>
            </div>
          </blockquote>
        </div>
      `;
      document.querySelector('#emails-view').append(element);

      document.querySelector(`#email-${email.id}`).addEventListener('click', () => {
        show_email(email.id);
      });
    });

  })
}
// REACT FUNCTIONS, but they didnt work somehow

// function Mail(props) {
//   return (
//     <div class="card">
//       <div class="card-header">
//         { props.subject }
//       </div>
//       <div class="card-body">
//         <blockquote class="blockquote mb-0">
//           <p> { props.body } </p>
//           <footer class="blockquote-footer">Sent to <cite title="Source Title">{ props.recipients }</cite></footer>
//         </blockquote>
//       </div>
//     </div>
//   )
// }

// function SentMails() {
//   let return_value;

//   fetch("emails/sent", {
//     method: "GET",
//   })
//   .then(response => response.json())
//   .then(result => {
//     console.log(result);
//     return_value = <Mail props={ result[0] }/>;
//   })
//   return (
//     <div>
//       { return_value }
//     </div>
//   )
// }