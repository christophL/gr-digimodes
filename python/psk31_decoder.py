
import numpy
import pmt
import sys
import digimodes

from gnuradio import gr, blocks

class psk31_decoder(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name = "psk31_decoder",
            in_sig = [numpy.uint8],
            out_sig = None,
        )
        self.nz = 0
        self.curr = ""
        self.out_string = ""
        self.rev_varicodes = dict()
        self.message_port_register_out(pmt.intern('out'))

        for k in digimodes.varicodes.keys():
            self.rev_varicodes[digimodes.varicodes[k]] = k

    def work(self, input_items, output_items):

        for i in input_items[0]:

            #print i
            if i == 0:
                i = 1
            else:
                i = 0

            if i == 0:
                self.nz += 1

                if self.nz == 2:
                    if self.rev_varicodes.has_key(self.curr):
                        c = self.rev_varicodes[self.curr]
                        self.out_string += c
                        sys.stdout.write(c)
                        if c == "\n":
                           print "sent pdu"
                           payload = pmt.make_u8vector(len(self.out_string), 0)
                           j = 0
                           for a in self.out_string:
                               pmt.u8vector_set(payload, j, ord(a)) 
                               j += 1
                           self.message_port_pub(pmt.intern('out'), pmt.cons(pmt.PMT_NIL, payload))
                           self.out_string = ""

                    self.nz = 0
                    self.curr = ""
                    sys.stdout.flush()

            elif i == 1:
                if self.nz == 1 and self.curr != "":
                    self.curr += "0"
                self.curr += "1"
                self.nz = 0

        
        return len(input_items[0])

