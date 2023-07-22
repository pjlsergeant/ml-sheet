import xlsxwriter
from micrograd import nn
from micrograd.engine import Value
from sklearn import datasets
from llmsheet.formatter import Formatter

from llmsheet.from_micrograd import render_micrograd_mlp
from llmsheet.xl_position import XLPosition

# load iris dataset
iris = datasets.load_iris()

workbook = xlsxwriter.Workbook("demo.xlsx")
f = Formatter.lazy(workbook)
worksheet = workbook.add_worksheet()

# Print out the input names
worksheet.write('A1', "Feature")
worksheet.write('A2', "Value")
cursor = XLPosition.from_str('B1')
inputs = []

for feature in iris.feature_names:
    worksheet.write( str(cursor), feature )
    worksheet.write( str(cursor.from_offset(0, 1)), 1 )
    inputs.append( cursor.from_offset(0, 1) )
    cursor = cursor.from_offset(1,0)

# Print the output names
outputs = []
cursor = XLPosition.from_str('B8')

for label in iris.target_names:
    worksheet.write( str(cursor), label )
    worksheet.write( str(cursor.from_offset(1, 0)), 1 )
    outputs.append( cursor.from_offset(1, 0) )
    cursor = cursor.from_offset(0,1)

# Wrangle the data into micrograd form
X = iris.data
y = iris.target

def make_y(i):
    vv = [Value(0), Value(0), Value(0)]
    vv[i] = Value(1)
    return vv

X = [list(map(Value, x_row)) for x_row in X]
y = [make_y(i) for i in y]

# Create the network itself
network = nn.MLP( 4, [16, 16, 16, 3])

learning_rate = 0.0005
n_epochs = 100

# training loop
for epoch in range(n_epochs):
    epoch_loss = 0

    for (sample_x, sample_y) in zip( X, y ):
        prediction = network(sample_x)
        sample_loss = sum((p - a)**2 for p, a in zip(prediction, sample_y))
        epoch_loss += sample_loss

        sample_loss.backward()

        # gradient descent
        for param in network.parameters():
            param.data -= learning_rate * param.grad
            param.grad = 0  # reset gradient to zero after the update

    if epoch % 5 == 0:
        print(f'Epoch: {epoch}, Loss: {(epoch_loss/len(X)).data}')

linear_outputs = render_micrograd_mlp(worksheet,f, network, inputs, XLPosition.from_str('H2'))
for (f,t) in zip(linear_outputs, outputs):
    worksheet.write(str(t), '=' + str(f))
workbook.close()