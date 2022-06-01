	.file	"ct.c"
	.option nopic
	.attribute arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0"
	.attribute unaligned_access, 0
	.attribute stack_align, 16
	.text
	.align	1
	.globl	ccopy
	.type	ccopy, @function
ccopy:
	negw	a2,a2
	xor	a0,a0,a1
	and	a0,a0,a2
	xor	a0,a1,a0
	sext.w	a0,a0
	ret
	.size	ccopy, .-ccopy
	.align	1
	.globl	test_ccopy_loop
	.type	test_ccopy_loop, @function
test_ccopy_loop:
	addi	sp,sp,-64
	addiw	a0,a0,7
	sd	s5,8(sp)
	sraiw	s5,a0,3
	sd	s0,48(sp)
	sd	s1,40(sp)
	sd	s2,32(sp)
	sd	s3,24(sp)
	sd	s4,16(sp)
	slliw	s0,s5,3
	sd	ra,56(sp)
	mv	s2,a1
	mv	s3,a2
	mv	s4,a3
	li	a0,0
	li	s1,0
	addi	s5,s5,-1
.L3:
	bne	s0,s1,.L4
	ld	ra,56(sp)
	ld	s0,48(sp)
	ld	s1,40(sp)
	ld	s2,32(sp)
	ld	s3,24(sp)
	ld	s4,16(sp)
	ld	s5,8(sp)
	addi	sp,sp,64
	jr	ra
.L4:
	srliw	a5,s1,3
	sub	a5,s5,a5
	add	a5,s2,a5
	lbu	a2,0(a5)
	andi	a5,s1,7
	mv	a1,s4
	sraw	a2,a2,a5
	andi	a2,a2,1
	mv	a0,s3
	call	ccopy
	sext.w	a0,a0
	addiw	s1,s1,1
	j	.L3
	.size	test_ccopy_loop, .-test_ccopy_loop
	.section	.rodata.str1.8,"aMS",@progbits,1
	.align	3
.LC0:
	.string	"\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252\252"
	.section	.text.startup,"ax",@progbits
	.align	1
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-160
	li	a2,128
	lla	a1,.LC0
	addi	a0,sp,16
	sd	ra,152(sp)
	call	memcpy
	li	a5,-16535552
	addi	a5,a5,580
	sw	a5,8(sp)
	li	a5,-559038464
	addi	a5,a5,-273
	sw	a5,12(sp)
	lw	a2,8(sp)
	lw	a3,12(sp)
	addi	a1,sp,16
	sext.w	a2,a2
	sext.w	a3,a3
	li	a0,100
	call	test_ccopy_loop
	sext.w	a0,a0
	sw	a0,4(sp)
 #APP
# 48 "ct.c" 1
	addi x0, x1, 0
	
# 0 "" 2
 #NO_APP
	lw	a2,8(sp)
	lw	a3,12(sp)
	addi	a1,sp,16
	sext.w	a2,a2
	sext.w	a3,a3
	li	a0,100
	call	test_ccopy_loop
	ld	ra,152(sp)
	sext.w	a0,a0
	sw	a0,4(sp)
	li	a0,0
	addi	sp,sp,160
	jr	ra
	.size	main, .-main
	.ident	"GCC: (GNU) 9.2.0"
