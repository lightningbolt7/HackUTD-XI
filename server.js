const express = require('express');
const bodyParser = require('body-parser');
const sgMail = require('@sendgrid/mail');
const cors = require('cors');



const app = express();
app.use(bodyParser.json());
app.use(cors());

sgMail.setApiKey('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');

// Endpoint to send email
app.post('/send-email', (req, res) => {
    const { to, subject, text } = req.body;

    // console.log({body})

    const msg = {
        to: to,
        from: 'xpop218@gmail.com', // Use your verified SendGrid sender email
        subject: subject,
        text,
        // content: text
    };

    sgMail
        .send(msg)
        .then(() => res.status(200).json({ success: true }))
        .catch(error => {
            // console.error(error.response.body);

            res.status(500).json({ success: false, error: error.message });
        });
});

app.listen(3000, () => console.log('Server is running on port 3000'));