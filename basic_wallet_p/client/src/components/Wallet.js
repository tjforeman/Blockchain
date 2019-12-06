import React from 'react'

const Wallet = (props) => {

const amount_sent = props.sent.map(amount=>{
    return amount.amount
})

let total_sent = 0

for(var i = 0, len = amount_sent.length; i < len; i++) {
    total_sent += amount_sent[i]
}

const amount_received = props.recieved.map(amount =>{
    return amount.amount
})

let total_received = 0
for(var i = 0, len = amount_received.length; i < len; i++) {
    total_received += amount_received[i]
}

console.log(total_received)
console.log(total_sent)


if(props.sent == undefined && props.recieved == undefined){
return(
    <p>Please enter your id</p>
)
}
else{
    return(
        <div>
            <div>
    <h2>Current Ballance: {total_received - total_sent}</h2>
            </div>
            {props.sent.map(sent =>{
                return(<div>
                    <p>Payed to: {sent.recipient}</p>
                    <p>Amount sent: {sent.amount}</p>
                </div>)
            })}

             {props.recieved.map(recieved =>{
                return(<div>
                    <p>Payed from: {recieved.sender}</p>
                    <p>Amount received: {recieved.amount}</p>
                </div>)
            })}
        </div>
    )

}
}


export default Wallet