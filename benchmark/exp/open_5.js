/**
* Copyright 2017 HUAWEI. All Rights Reserved.
*
* SPDX-License-Identifier: Apache-2.0
*
*/

'use strict';

module.exports.info  = 'opening accounts';

let account_array = [];
let txnPerBatch;
let initMoney;
let bc, contx;
module.exports.init = function(blockchain, context, args) {
    if(!args.hasOwnProperty('money')) {
        return Promise.reject(new Error('simple.open - \'money\' is missed in the arguments'));
    }

    if(!args.hasOwnProperty('txnPerBatch')) {
        args.txnPerBatch = 1;
    }
    initMoney = args.money;
    txnPerBatch = args.txnPerBatch;
    bc = blockchain;
    contx = context;
    return Promise.resolve();
};

const dic = 'abcdefghijklmnopqrstuvwxyz';
/**
 * Generate string by picking characters from dic variable
 * @param {*} number character to select
 * @returns {String} string generated based on @param number
 */
function get26Num(number){
    let result = '';
    while(number > 0) {
        result += dic.charAt(number % 26);
        number = parseInt(number/26);
    }
    return result;
}

let prefix;
/**
 * Generate unique account key for the transaction
 * @returns {String} account key
 */
function generateAccount(number) {
    // should be [a-z]{1,9}
    if(typeof prefix === 'undefined') {
        prefix = get26Num(process.pid);
    }
    return prefix + get26Num(account_array.length+1+number);
}

/**
 * Generates simple workload
 * @returns {Object} array of json objects
 */
function generateWorkload() {
    let workload = [];
    for(let i= 0; i < txnPerBatch; i++) {
        let acc_id = generateAccount(0);
        let acc_id_2 = generateAccount(1);
        let acc_id_3 = generateAccount(2);
        let acc_id_4 = generateAccount(3);
        let acc_id_5 = generateAccount(4);
        account_array.push(acc_id);
        account_array.push(acc_id_2);
        account_array.push(acc_id_3);
        account_array.push(acc_id_4);
        account_array.push(acc_id_5);
        let acc = {
            'verb': 'open',
            'account': acc_id,
            'money': initMoney,
            'account_2': acc_id_2,
            'money_2': initMoney,
            'account_3': acc_id_3,
            'money_3': initMoney,
            'account_4': acc_id_4,
            'money_4': initMoney,
            'account_5': acc_id_5,
            'money_5': initMoney
        };
        workload.push(acc);
    }
    return workload;
}

module.exports.run = function() {
    let args = generateWorkload();
    //console.log(args);
    return bc.invokeSmartContract(contx, 'simple', 'v0', args, 30);
};

module.exports.end = function() {
    return Promise.resolve();
};

module.exports.account_array = account_array;
