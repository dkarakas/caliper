/**
* Copyright 2017 HUAWEI. All Rights Reserved.
*
* SPDX-License-Identifier: Apache-2.0
*
*/

package main

import (
	"fmt"
	"strconv"

	"github.com/hyperledger/fabric/core/chaincode/shim"
	pb "github.com/hyperledger/fabric/protos/peer"
)

const ERROR_SYSTEM = "{\"code\":300, \"reason\": \"system error: %s\"}"
const ERROR_WRONG_FORMAT = "{\"code\":301, \"reason\": \"command format is wrong\"}"
const ERROR_ACCOUNT_EXISTING = "{\"code\":302, \"reason\": \"account already exists\"}"
const ERROR_ACCOUNT_ABNORMAL = "{\"code\":303, \"reason\": \"abnormal account\"}"
const ERROR_MONEY_NOT_ENOUGH = "{\"code\":304, \"reason\": \"account's money is not enough\"}"



type SimpleChaincode struct {

}

func (t *SimpleChaincode) Init(stub shim.ChaincodeStubInterface) pb.Response {
	// nothing to do
	return shim.Success(nil)
}

func (t *SimpleChaincode) Invoke(stub shim.ChaincodeStubInterface) pb.Response {
	function, args := stub.GetFunctionAndParameters()

	if function == "open" {
		return t.Open(stub, args)
	}
	if function == "delete" {
		return t.Delete(stub, args)
	}
	if function == "query" {
		return t.Query(stub, args)
	}
	if function == "transfer" {
		return t.Transfer(stub, args)
	}

	return shim.Error(ERROR_WRONG_FORMAT)
}

// open an account, should be [open account money]
func (t *SimpleChaincode) Open(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	if len(args) != 10 {
		return shim.Error(ERROR_WRONG_FORMAT)
	}

	account  := args[0]
	account_2  := args[2]
	account_3  := args[4]
	account_4  := args[6]
	account_5  := args[8]


	money,err := stub.GetState(account)
	if money != nil {
		return shim.Error(ERROR_ACCOUNT_EXISTING)
	}
	money_2,err_2 := stub.GetState(account_2)
	if money_2 != nil {
		return shim.Error(ERROR_ACCOUNT_EXISTING)
	}
	money_3,err_3 := stub.GetState(account_3)
	if money_3 != nil {
		return shim.Error(ERROR_ACCOUNT_EXISTING)
	}
	money_4,err_4 := stub.GetState(account_4)
	if money_4 != nil {
		return shim.Error(ERROR_ACCOUNT_EXISTING)
	}
	money_5,err_5 := stub.GetState(account_5)
	if money_5 != nil {
		return shim.Error(ERROR_ACCOUNT_EXISTING)
	}



	_,err = strconv.Atoi(args[1])
	if err != nil {
		return shim.Error(ERROR_WRONG_FORMAT)
	}
	_,err_2 = strconv.Atoi(args[3])
	if err_2 != nil {
		return shim.Error(ERROR_WRONG_FORMAT)
	}
	_,err_3 = strconv.Atoi(args[5])
	if err_3 != nil {
		return shim.Error(ERROR_WRONG_FORMAT)
	}
	_,err_4 = strconv.Atoi(args[7])
	if err_4 != nil {
		return shim.Error(ERROR_WRONG_FORMAT)
	}
	_,err_5 = strconv.Atoi(args[9])
	if err_5 != nil {
		return shim.Error(ERROR_WRONG_FORMAT)
	}



	err = stub.PutState(account, []byte(args[1]))
	if err != nil {
		s := fmt.Sprintf(ERROR_SYSTEM, err.Error())
		return shim.Error(s)
	}
	err_2 = stub.PutState(account_2, []byte(args[3]))
	if err_2 != nil {
		s := fmt.Sprintf(ERROR_SYSTEM, err.Error())
		return shim.Error(s)
	}
	err_3 = stub.PutState(account_3, []byte(args[5]))
	if err_3 != nil {
		s := fmt.Sprintf(ERROR_SYSTEM, err.Error())
		return shim.Error(s)
	}
	err_4 = stub.PutState(account_4, []byte(args[7]))
	if err_4 != nil {
		s := fmt.Sprintf(ERROR_SYSTEM, err.Error())
		return shim.Error(s)
	}
	err_5 = stub.PutState(account_5, []byte(args[9]))
	if err_5 != nil {
		s := fmt.Sprintf(ERROR_SYSTEM, err.Error())
		return shim.Error(s)
	}




	return shim.Success(nil)
}

// delete an account, should be [delete account]
func (t *SimpleChaincode) Delete(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	if len(args) != 1 {
		return shim.Error(ERROR_WRONG_FORMAT)
	}

	err := stub.DelState(args[0])
	if err != nil {
		s := fmt.Sprintf(ERROR_SYSTEM, err.Error())
		return shim.Error(s)
	}

	return shim.Success(nil)
}

// query current money of the account,should be [query accout]
func (t *SimpleChaincode) Query(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	if len(args) != 1 {
		return shim.Error(ERROR_WRONG_FORMAT)
	}

	money, err := stub.GetState(args[0])
	if err != nil {
		s := fmt.Sprintf(ERROR_SYSTEM, err.Error())
		return shim.Error(s)
	}

	if money == nil {
		return shim.Error(ERROR_ACCOUNT_ABNORMAL)
	}

	return shim.Success(money)
}

// transfer money from account1 to account2, should be [transfer account1 account2 money]
func (t *SimpleChaincode) Transfer(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	if len(args) != 3 {
		return shim.Error(ERROR_WRONG_FORMAT)
	}
	money, err := strconv.Atoi(args[2])
	if err != nil {
		return shim.Error(ERROR_WRONG_FORMAT)
	}

	moneyBytes1, err1 := stub.GetState(args[0])
	moneyBytes2, err2 := stub.GetState(args[1])
	if err1 != nil || err2 != nil {
		s := fmt.Sprintf(ERROR_SYSTEM, err.Error())
		return shim.Error(s)
	}
	if moneyBytes1 == nil || moneyBytes2 == nil {
		return shim.Error(ERROR_ACCOUNT_ABNORMAL)
	}

	money1, _ := strconv.Atoi(string(moneyBytes1))
	money2, _ := strconv.Atoi(string(moneyBytes2))
	if money1 < money {
		return shim.Error(ERROR_MONEY_NOT_ENOUGH)
	}

	money1 -= money
	money2 += money

	err = stub.PutState(args[0], []byte(strconv.Itoa(money1)))
	if err != nil {
		s := fmt.Sprintf(ERROR_SYSTEM, err.Error())
		return shim.Error(s)
	}

	err = stub.PutState(args[1], []byte(strconv.Itoa(money2)))
	if err != nil {
		s := fmt.Sprintf(ERROR_SYSTEM, err.Error())
		return shim.Error(s)
	}

	return shim.Success(nil)
}


func  main()  {
	err := shim.Start(new(SimpleChaincode))
	if err != nil {
		fmt.Printf("Error starting chaincode: %v \n", err)
	}

}