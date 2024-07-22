

def fx(stock, trials=10000):
    qdata = X.price_history(stock, full_time=True)['candles']
    price_array = [row['open'] for row in qdata]

    wins = 0
    skip_trials = 0
    
    plot = False

    for j in range(trials):

        random_index = random.randrange(0, len(price_array) - 22, 1)

        init_datetime = float(qdata[random_index]['datetime'])
        skip = False
        for i in range(random_index + 1, random_index + 20):
            row_date_time = float(qdata[i]['datetime'])

            if row_date_time == (init_datetime + 60000):
                pass
            else:
                #print('intra day data selection, breakpoint')
                #print(str(wins) + ' wins out of '+ str(j)+ ' trials, with '+ str(skip_trials)+ ' skipped trials')
                #print(row_date_time)
                #print(init_datetime)
                skip_trials+=1
                skip= True

            init_datetime = row_date_time

        if skip:
            pass
        else:


            cost_basis = []
            #print(random_index)
            #print(price_array[random_index:random_index+20])
            window_price_array = price_array[random_index:random_index+20]

            for i in range(random_index, random_index+20):

                cost_basis.append(sum(price_array[random_index:i+1])/((i-random_index)+1))

            profit_loss_at_open = []
            max_profit_loss = []

            shares = 1

            #print(qdata[random_index:random_index+20])

            for row in qdata[random_index:random_index+20]:
                high = row['high']

                #print('high price: '+ str(high))
                #print('open price of minute: '+ str(window_price_array[shares-1]))

                pl = (window_price_array[shares-1] - cost_basis[shares-1]) * shares
                max_profit = (high - cost_basis[shares-1]) * shares
                profit_loss_at_open.append(pl)
                max_profit_loss.append(max_profit)

                shares += 1

            value = max(max_profit_loss)
            print(value)
            
            if plot:
                    
                plt.subplot(2,1,1)
                plt.title('Profit and Loss (g - high prices) (r - open price)')
                plt.plot(max_profit_loss, color='g')
                plt.plot(profit_loss_at_open, color= 'r')
    
                plt.subplot(2, 1, 2)
                plt.title('Price of asset and cost basis (blue)')
                plt.plot(window_price_array, color = 'black')
                plt.plot(cost_basis, color = 'blue')
    
                plt.subplots_adjust(left=0.1,
                                    bottom=0.1,
                                    right=0.9,
                                    top=0.9,
                                    wspace=0.4,
                                    hspace=0.4)
            else:
                pass

            plt.show()

            for pl in max_profit_loss:
                if pl>0:
                    #print(max_profit_loss)
                    wins+=1

                    break
                else:
                    pass




                    #print('win')


            '''plt.subplot(1,2,1)
            plt.plot(max_profit_loss, color='g')
            plt.plot(profit_loss_at_open)
        
            plt.subplot(1,2,2)
            plt.plot(window_price_array)
        
            plt.show()'''


    print(str(wins) + ' wins out of '+ str(j)+ ' trials, with '+ str(skip_trials)+ ' skipped trials')



