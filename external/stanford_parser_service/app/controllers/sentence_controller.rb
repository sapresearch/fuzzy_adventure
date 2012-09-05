class SentenceController < ApplicationController

	def parse
		sentence = params[:sentence]
		parsed = Sentence.parse(sentence)
		respond_to do |format|
			format.json { render :json => parsed }
		end
	end

end
