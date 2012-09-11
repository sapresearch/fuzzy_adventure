class SentenceController < ApplicationController

	def parse
		sentence = params[:sentence]
		sentence.gsub!("_", " ")
		parsed = Sentence.parse(sentence).to_s
		respond_to do |format|
			format.json { render :json => parsed }
		end
	end

end
