export const htmlContent = (items) => { `
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pdf Content</title>
        <style>
            body {
                font-size: 16px;
                color: rgb(255, 196, 0);
            }
            li {
                text-align: center;
            }
        </style>
    </head>
    <body>
        <ul>
            ${items.map(
                (item, idx) => <li key={idx}>{item.quantity}x - {item.name} </li>
            )}
        </ul>
    </body>
    </html>
`};