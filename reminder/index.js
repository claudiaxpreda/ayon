require('dotenv').config()

const express = require('express')
const nodemailer = require('nodemailer')
const fs = require('fs')
const promMid = require('express-prometheus-middleware');

const app = express()

app.use(promMid({
  metricsPath: '/metrics',
  collectDefaultMetrics: true,
  requestDurationBuckets: [0.1, 0.5, 1, 1.5],
}));

app.use(express.json())


let transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.EMAIL,
    pass: process.env.PASSWORD
  }
})

app.post('/api/notify', async (req, res) => {
  const { email, plan } = req.body
  fs.readFile('template.html', { encoding: 'utf-8' }, (err, html) => {
    if (err) {
      console.log(err)
    } else {
      plan.map(item => html += `<tr class='item last'><td>${item.title}</td><td>${item.location}</td><td>${item.time}</td><td>${item.details}</td></tr>`)
      html += '</table></div></body></html>'

      const mailOptions = {
        from: process.env.EMAIL,
        to: email,
        subject: "Today's plan from Ayon",
        html
      }

      transporter.sendMail(mailOptions, (err, data) => {
        if (err) {
          console.log('Error occured')
          return res.status(500).send('Error occured')
        } else {
          console.log('Email sent')
          return res.status(200).send('Email sent')
        }
      })
    }
  })
})

app.listen(process.env.PORT || 3000, () =>
  console.log(`👂 Listening on: ${process.env.PORT || 3000}`)
)