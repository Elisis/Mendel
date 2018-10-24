from llvmlite import ir


class Number():
	def __init__(self, builder, module, value):
		self.builder = builder
		self.module = module
		self.value = value
	
	def eval(self):
		i = ir.Constant(ir.IntType(8), int(self.value))
		return i
	
class BinaryOp():
	def __init__(self, builder, module, left, right):
		self.builder = builder
		self.module = module
		self.left = left
		self.right = right
		
class Sum(BinaryOp):
	def eval(self):
		i = self.builder.add(self.left.eval(), self.right.eval())
		return i

class Sub(BinaryOp):
	def eval(self):
		i = self.builder.sub(self.left.eval(), self.right.eval())
		return i
		
class Multiply(BinaryOp):
	def eval(self):
		i = self.builder.multiply
		
class Out():
	def __init__(self, builder, module, outf, value):
		self.builder = builder
		self.module = module
		self.outf = outf
		self.value = value
		
	
	def eval(self):
		value = self.value.eval()
		
		#Declare an argument list
		voidptr_ty = ir.IntType(8).as_pointer()
		fmt = "%i \n\0"
		c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
							bytearray(fmt.encode("utf-8")))
		
		global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="fstr")
		global_fmt.linkage = 'internal'
		global_fmt.global_constant = True
		global_fmt.initializer = c_fmt
		fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)
		
		#Call Out Function
		self.builder.call(self.outf, [fmt_arg, value])
		
